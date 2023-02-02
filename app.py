import os
import bcrypt
from glob import glob

from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth

from gevent.pywsgi import WSGIServer

from simple_schema_validator import schema_validator

from pandas import errors as pd_errors

from src.configuration import Configuration
from src.utils import APIKey

from src.processing import EMG
from src.processing import IMU
from src.processing import Areas

from src.helpers import PDFHelper

app = Flask(__name__)

auth = HTTPTokenAuth(header='X-API-Key')
api_key_hashed = APIKey.hash_key(Configuration.API_KEY.value)


def validate_request_body(body, schema):
    validation = schema_validator(schema, body)

    if not validation:
        if len(validation.additional_keys) > 0:
            details = 'data contain more keys than expected'
        elif len(validation.missing_keys) > 0:
            details = 'data contain less keys than expected'
        elif len(validation.type_errors) > 0:
            details = 'data contain keys which don\'t match expected type'
        else:
            details = None

        return {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f'Request body is not properly formatted',
                "details": details
            }
        }
    else:
        return True


@auth.verify_token
def verify_apikey(key):
    return bcrypt.checkpw(key.encode('utf-8'), api_key_hashed)


@app.route('/imu/', methods=['POST'])
@auth.login_required
def generate_imu_analysis():
    body = request.json

    schema = {
        'data_path': str,
        'analysis': str,
        'participants': [str],
    }

    validation = validate_request_body(body, schema)

    if validation is not True:
        return jsonify(validation), 400

    data_path_parameter = os.path.normpath(body['data_path'])

    for participant in body['participants']:
        data_path = os.path.join(data_path_parameter, body['analysis'], participant)
        csv_files = glob(os.path.join(data_path, "*.csv"))

        if len(csv_files) > 0:
            for csv_file in csv_files:
                csv_filename, _ = os.path.basename(csv_file).rsplit('.', 1)
                files = os.listdir(os.path.join(data_path_parameter, '.metadata', f'.{body["analysis"]}', participant))

                if f'plot_angle_{csv_filename}.svg' not in files or \
                        f'small_angle_{csv_filename}.json' not in files:
                    imu = None
                    try:
                        imu = IMU(data_path_parameter, csv_file)
                    except pd_errors.ParserError:
                        if imu is not None:
                            error = f'Error occurs while trying to read: {imu.get_csv_path()[1]}'
                        else:
                            error = 'Error occurs while trying to read CSV files'

                        output = {
                            "code": 500,
                            "status": "failed",
                            "payload": {
                                "message": error,
                                "details": None
                            }
                        }
                        return jsonify(output), 500

                    try:
                        imu.start_processing()
                    except Exception as e:
                        output = {
                            "code": 500,
                            "status": "failed",
                            "payload": {
                                "message": f'Error occurs while trying to process IMU data. Related file: '
                                           f'{imu.get_csv_path()[1]}',
                                "details": str(e)
                            }
                        }
                        return jsonify(output), 500
        else:
            output = {
                "code": 404,
                "status": "failed",
                "payload": {
                    "message": f'No CSV files found in path: {data_path}',
                    "details": None
                }
            }
            return jsonify(output), 404

    output = {
        "code": 201,
        "status": "created",
        "payload": {
            "data_path": body['data_path'],
            "analysis": body['analysis'],
            "participants": body['participants']
        }
    }
    return jsonify(output), 201


@app.route('/emg/', methods=['POST'])
@auth.login_required
def generate_emg_analysis():
    body = request.json

    schema = {
        'window_size': float,
        'data_path': str,
        'analysis': str,
        'stage': str,
        'participant': str,
        'iteration': int,
        'point_x': float,
        'point_y': float
    }

    validation = validate_request_body(body, schema)

    if validation is not True:
        return jsonify(validation), 400

    data_path = os.path.join(os.path.normpath(body['data_path']), body['analysis'], body['participant'])
    csv_files = glob(os.path.join(data_path, "*.csv"))

    if len(csv_files) > 0:
        try:
            csv_file = csv_files[body['iteration']]
        except IndexError:
            output = {
                "code": 404,
                "status": "failed",
                "payload": {
                    "message": f'cannot find a CSV file for iteration {body["iteration"]}',
                    "details": None
                }
            }
            return jsonify(output), 500

        emg = None

        try:
            emg = EMG(body['data_path'], csv_file, body['stage'])
        except pd_errors.ParserError:
            if emg is not None:
                error = f'Error occurs while trying to read: {emg.get_csv_path()[1]}'
            else:
                error = 'Error occurs while trying to read CSV files'

            output = {
                "code": 500,
                "status": "failed",
                "payload": {
                    "message": error,
                    "details": None
                }
            }
            return jsonify(output), 500

        emg.start_processing(body['window_size'], body['point_x'], body['point_y'])
    else:
        output = {
            "code": 404,
            "status": "failed",
            "payload": {
                "message": f'No CSV file founded in path: {data_path}',
                "details": None
            }
        }
        return jsonify(output), 404

    output = {
        "code": 201,
        "status": "created",
        "payload": {
            "data_path": body['data_path'],
            "analysis": body['analysis'],
            "stage": body['stage'],
            "iteration": body['iteration'],
            "participant": body['participant']
        }
    }
    return jsonify(output), 201


@app.route('/areas/', methods=['POST'])
@auth.login_required
def generate_areas():
    body = request.json

    schema = {
        'data_path': str,
        'analysis': str,
        'stage': str,
        'participants': [str]
    }

    validation = validate_request_body(body, schema)

    if validation is not True:
        return jsonify(validation), 400

    for participant in body['participants']:
        data_path = os.path.join(os.path.normpath(body['data_path']), '.metadata', f'.{body["analysis"]}', participant)
        csv_files = glob(os.path.join(data_path, f'envelope_{body["stage"]}_*.csv'))

        if len(csv_files) > 0:
            try:
                areas = Areas(data_path, csv_files)
            except pd_errors.ParserError:
                error = 'Error occurs while trying to read CSV files'

                output = {
                    "code": 500,
                    "status": "failed",
                    "payload": {
                        "message": error,
                        "details": None
                    }
                }
                return jsonify(output), 500

            try:
                areas.start_processing()
            except Exception as e:
                output = {
                    "code": 500,
                    "status": "failed",
                    "payload": {
                        "message": f'Error occurs while trying to process areas',
                        "details": str(e)
                    }
                }
                return jsonify(output), 500

        else:
            output = {
                "code": 404,
                "status": "failed",
                "payload": {
                    "message": f'No CSV files found in path: {data_path}',
                    "details": None
                }
            }
            return jsonify(output), 404

    output = {
        "code": 201,
        "status": "created",
        "payload": {
            "data_path": body['data_path'],
            "analysis": body['analysis'],
            "stage": body['stage'],
            "participants": body['participants']
        }
    }
    return jsonify(output), 201


@app.route('/report/', methods=['POST'])
@auth.login_required
def generate_report():
    body = request.json

    schema = {
        'data_path': str,
        'analysis': str
    }

    validation = validate_request_body(body, schema)

    if validation is not True:
        return jsonify(validation), 400

    base_path = os.path.join(os.path.normpath(body['data_path']), '.metadata', f'.{body["analysis"]}')
    html_path = os.path.join(base_path, f'{body["analysis"]}_report.html')
    output_path = os.path.join(base_path, f'{body["analysis"]}_report.pdf')

    try:
        PDFHelper.generate_pdf_from_html(html_path, output_path)
    except Exception as e:
        output = {
            "code": 500,
            "status": "failed",
            "payload": {
                "message": f'Error occurs while trying to generate PDF report',
                "details": str(e)
            }
        }
        return jsonify(output), 500

    output = {
        "code": 201,
        "status": "created",
        "payload": {
            "data_path": body['data_path'],
            "analysis": body['analysis']
        }
    }
    return jsonify(output), 201


def main():
    http = WSGIServer((Configuration.HOST.value, Configuration.PORT.value), app.wsgi_app)
    http.serve_forever()


if __name__ == '__main__':
    main()
