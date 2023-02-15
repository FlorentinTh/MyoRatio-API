from gevent import monkey

monkey.patch_all()

import os
from glob import glob
from typing import Optional

import bcrypt
from dask.base import compute
from dask.delayed import delayed
from flask import Flask, Response, jsonify, request
from flask_httpauth import HTTPTokenAuth
from gevent.pywsgi import WSGIServer
from pandas import errors as pd_errors
from simple_schema_validator import schema_validator

from configuration import Configuration
from src.helpers import JSONHelper, PDFHelper
from src.processing import EMG, IMU, Areas, Points, Results
from src.utils import APIKey

app = Flask(__name__)

auth = HTTPTokenAuth(header="X-API-Key")
api_key_hashed = APIKey.hash_key(Configuration.API_KEY.value)


def validate_request_body(body: dict, schema: dict) -> Optional[str]:
    validation = schema_validator(schema, body)

    details = None

    if validation is not None:
        if not validation:
            if len(validation.additional_keys) > 0:
                details = "data contain more keys than expected"
            elif len(validation.missing_keys) > 0:
                details = "data contain less keys than expected"
            elif len(validation.type_errors) > 0:
                details = "data contain keys which don't match expected type"

    return details


@auth.verify_token
def verify_api_key(key) -> bool:
    return bcrypt.checkpw(key.encode("utf-8"), api_key_hashed)


@delayed
def parallel_imu_processing(body: dict, participant: str) -> Optional[dict]:
    data_path_parameter = os.path.normpath(body["data_path"])
    data_path = os.path.join(
        data_path_parameter, "analysis", body["analysis"], participant
    )
    csv_files = glob(os.path.join(data_path, "*.csv"))

    if len(csv_files) > 0:
        for csv_file in csv_files:
            csv_filename, _ = os.path.basename(csv_file).rsplit(".", 1)
            files = os.listdir(
                os.path.join(
                    data_path_parameter,
                    "analysis",
                    ".metadata",
                    body["analysis"],
                    participant,
                )
            )

            if f"small_angle_{csv_filename}.json" not in files:
                imu = None
                try:
                    imu = IMU(data_path_parameter, csv_file, body["analysis"])
                except pd_errors.ParserError as error:
                    if imu is not None:
                        message = (
                            f"Error occurs while trying to read: {imu.get_csv_path()[1]}"
                        )
                    else:
                        message = "Error occurs while trying to read CSV files"

                    return {
                        "code": 500,
                        "status": "failed",
                        "payload": {"message": message, "details": str(error)},
                    }

                try:
                    imu.start_processing()
                except Exception as e:
                    return {
                        "code": 500,
                        "status": "failed",
                        "payload": {
                            "message": f"Error occurs while trying to process IMU data. Related file: "
                            f"{imu.get_csv_path()[1]}",
                            "details": str(e),
                        },
                    }
    else:
        return {
            "code": 404,
            "status": "failed",
            "payload": {
                "message": "Missing data",
                "details": f"No CSV files found in path: {data_path}",
            },
        }


@app.route("/imu/", methods=["POST"])
@auth.login_required
def generate_imu_analysis() -> tuple[Response, int]:
    body = request.json

    if body is None:
        output = {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f"Request body is not properly formatted",
                "details": "request body is empty",
            },
        }

        return jsonify(output), 400

    else:
        schema = {
            "data_path": str,
            "analysis": str,
            "participants": [str],
        }

        validation = validate_request_body(body, schema)

        if validation is not None:
            output = {
                "code": 400,
                "status": "failed",
                "payload": {
                    "message": f"Request body is not properly formatted",
                    "details": validation,
                },
            }

            return jsonify(output), 400

        participants = []

        for participant in body["participants"]:
            # deepcode ignore XSS: already sanitized
            participants.append(parallel_imu_processing(body, participant))

        outputs = compute(participants)

        for i in range(len(outputs[0])):
            output = outputs[0][i]

            if output is not None:
                return jsonify(output), output["code"]

        output = {
            "code": 201,
            "status": "created",
            "payload": {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "participants": body["participants"],
            },
        }

        return jsonify(output), 201


@app.route("/emg/", methods=["POST"])
@auth.login_required
def generate_emg_analysis() -> tuple[Response, int]:
    body = request.json

    if body is None:
        output = {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f"Request body is not properly formatted",
                "details": "request body is empty",
            },
        }

        return jsonify(output), 400

    else:
        schema = {
            "window_size": float,
            "data_path": str,
            "analysis": str,
            "stage": str,
            "participant": str,
            "iteration": int,
            "point_1x": float,
            "point_2x": float,
        }

        validation = validate_request_body(body, schema)

        if validation is not None:
            output = {
                "code": 400,
                "status": "failed",
                "payload": {
                    "message": f"Request body is not properly formatted",
                    "details": validation,
                },
            }

            return jsonify(output), 400

        data_path = os.path.join(
            os.path.normpath(body["data_path"]),
            "analysis",
            body["analysis"],
            body["participant"],
        )

        csv_files = glob(os.path.join(data_path, "*.csv"))

        if len(csv_files) > 0:
            try:
                csv_file = csv_files[body["iteration"]]
            except IndexError as error:
                output = {
                    "code": 404,
                    "status": "failed",
                    "payload": {
                        "message": f'cannot find a CSV file for iteration {body["iteration"]}',
                        "details": str(error),
                    },
                }
                return jsonify(output), 500

            emg = None

            try:
                emg = EMG(body["data_path"], csv_file, body["stage"])
            except pd_errors.ParserError as error:
                if emg is not None:
                    message = (
                        f"Error occurs while trying to read: {emg.get_csv_path()[1]}"
                    )
                else:
                    message = "Error occurs while trying to read CSV files"

                output = {
                    "code": 500,
                    "status": "failed",
                    "payload": {"message": message, "details": str(error)},
                }

                return jsonify(output), 500

            try:
                emg.start_processing(
                    body["window_size"], body["point_1x"], body["point_2x"]
                )
            except Exception as error:
                output = {
                    "code": 500,
                    "status": "failed",
                    "payload": {
                        "message": "Error occurs while trying to process EMG data",
                        "details": str(error),
                    },
                }

                return jsonify(output), 500

        else:
            output = {
                "code": 404,
                "status": "failed",
                "payload": {
                    "message": "Missing data",
                    "details": f"No CSV file founded in path: {data_path}",
                },
            }
            return jsonify(output), 404

        output = {
            "code": 201,
            "status": "created",
            "payload": {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "stage": body["stage"],
                "iteration": body["iteration"],
                "participant": body["participant"],
            },
        }
        return jsonify(output), 201


@app.route("/points/", methods=["POST"])
@auth.login_required
def get_points_automatically() -> tuple[Response, int]:
    body = request.json

    if body is None:
        output = {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f"Request body is not properly formatted",
                "details": "request body is empty",
            },
        }

        return jsonify(output), 400

    else:
        schema = {
            "data_path": str,
            "analysis": str,
            "stage": str,
            "participant": str,
            "iteration": int,
        }

        validation = validate_request_body(body, schema)

        if validation is not None:
            return jsonify(validation), 400

        data_path = os.path.join(
            os.path.normpath(body["data_path"]),
            "analysis",
            ".metadata",
            body["analysis"],
            body["participant"],
        )

        json_files = glob(os.path.join(data_path, "small_*.json"))
        points = Points(body["stage"], json_files[body["iteration"]])
        points = points.get_points()

        output = {
            "code": 200,
            "status": "ok",
            "payload": {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "stage": body["stage"],
                "iteration": body["iteration"],
                "participant": body["participant"],
                "points": points,
            },
        }

        return jsonify(output), 200


@delayed
def parallel_results_processing(body: dict, participant: str) -> Optional[dict]:
    data_path = os.path.join(
        os.path.normpath(body["data_path"]),
        "analysis",
        ".metadata",
        body["analysis"],
        participant,
    )
    csv_files = glob(os.path.join(data_path, f'envelope_{body["stage"]}_*.csv'))

    if len(csv_files) > 0:
        try:
            areas = Areas(data_path, csv_files)
        except pd_errors.ParserError as error:
            return {
                "code": 500,
                "status": "failed",
                "payload": {
                    "message": "Error occurs while trying to read CSV files",
                    "details": str(error),
                },
            }

        try:
            areas = areas.start_processing()
            ratios = Results(areas, body["analysis"])
            JSONHelper.write_ratio_file(data_path, body["stage"], ratios.get_ratios())
        except Exception as error:
            return {
                "code": 500,
                "status": "failed",
                "payload": {
                    "message": f"Error occurs while trying to process areas",
                    "details": str(error),
                },
            }

    else:
        return {
            "code": 404,
            "status": "failed",
            "payload": {
                "message": "Missing data",
                "details": f"No CSV files found in path: {data_path}",
            },
        }


@app.route("/results/", methods=["POST"])
@auth.login_required
def generate_results() -> tuple[Response, int]:
    body = request.json

    if body is None:
        output = {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f"Request body is not properly formatted",
                "details": "request body is empty",
            },
        }

        return jsonify(output), 400

    else:
        schema = {"data_path": str, "analysis": str, "stage": str, "participants": [str]}

        validation = validate_request_body(body, schema)

        if validation is not None:
            output = {
                "code": 400,
                "status": "failed",
                "payload": {
                    "message": f"Request body is not properly formatted",
                    "details": validation,
                },
            }

            return jsonify(output), 400

        participants = []

        for participant in body["participants"]:
            # deepcode ignore XSS: already sanitized
            participants.append(parallel_results_processing(body, participant))

        outputs = compute(participants)

        for i in range(len(outputs[0])):
            output = outputs[0][i]

            if output is not None:
                # deepcode ignore XSS: already sanitized
                return jsonify(output), output["code"]

        output = {
            "code": 201,
            "status": "created",
            "payload": {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "stage": body["stage"],
                "participants": body["participants"],
            },
        }

        return jsonify(output), 201


@app.route("/report/", methods=["POST"])
@auth.login_required
def generate_report() -> tuple[Response, int]:
    body = request.json

    if body is None:
        output = {
            "code": 400,
            "status": "failed",
            "payload": {
                "message": f"Request body is not properly formatted",
                "details": "request body is empty",
            },
        }

        return jsonify(output), 400

    else:
        schema = {"data_path": str, "analysis": str}

        validation = validate_request_body(body, schema)

        if validation is not None:
            output = {
                "code": 400,
                "status": "failed",
                "payload": {
                    "message": f"Request body is not properly formatted",
                    "details": validation,
                },
            }

            return jsonify(output), 400

        base_path = os.path.join(
            os.path.normpath(body["data_path"]), "analysis", ".metadata", body["analysis"]
        )
        html_path = os.path.join(base_path, f'{body["analysis"]}_report.html')
        output_path = os.path.join(
            os.path.normpath(body["data_path"]),
            "analysis",
            f'{body["analysis"]}_report.pdf',
        )

        try:
            PDFHelper.generate_pdf_from_html(html_path, output_path)
        except Exception as error:
            output = {
                "code": 500,
                "status": "failed",
                "payload": {
                    "message": f"Error occurs while trying to generate PDF report",
                    "details": str(error),
                },
            }

            return jsonify(output), 500

        output = {
            "code": 201,
            "status": "created",
            "payload": {"data_path": body["data_path"], "analysis": body["analysis"]},
        }

        return jsonify(output), 201


def main():
    try:
        http = WSGIServer((Configuration.HOST.value, Configuration.PORT.value), app)
        http.serve_forever()
    except KeyboardInterrupt:
        http.stop()


if __name__ == "__main__":
    main()
