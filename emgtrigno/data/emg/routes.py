import os
from glob import glob

from flask import Blueprint, Response, request
from pandas import errors as pd_errors

from emgtrigno.api import API, ResponseStatus
from emgtrigno.api.auth import auth
from emgtrigno.api.helpers import FileHelper

from .emg import EMG

emg_blueprint = Blueprint("emg_blueprint", __name__)


@emg_blueprint.route("/emg/", methods=["POST"])
@auth.login_required
def generate_emg_analysis() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, f"Request body is not properly formatted", "request body is empty"
        )

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

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                400, f"Request body is not properly formatted", validation
            )

        data_path = os.path.join(
            FileHelper.get_analysis_folder_path(
                os.path.normpath(body["data_path"]), body["analysis"]
            ),
            body["participant"],
        )

        csv_files = glob(os.path.join(data_path, "*.csv"))

        if len(csv_files) > 0:
            try:
                csv_file = csv_files[body["iteration"]]
            except IndexError as error:
                # deepcode ignore XSS: already sanitized
                return API.error_response(
                    404,
                    f'cannot find a CSV file for iteration {body["iteration"]}',
                    str(error),
                )

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

                # deepcode ignore XSS: already sanitized
                return API.error_response(500, message, str(error))

            try:
                emg.start_processing(
                    body["window_size"], body["point_1x"], body["point_2x"]
                )
            except Exception as error:
                return API.error_response(
                    500, f"Error occurs while trying to process EMG data", str(error)
                )

        else:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                404, "Missing data", f"No CSV file founded in path: {data_path}"
            )

        body = {
            "data_path": body["data_path"],
            "analysis": body["analysis"],
            "stage": body["stage"],
            "iteration": body["iteration"],
            "participant": body["participant"],
        }

        # deepcode ignore XSS: already sanitized
        return API.success_response(201, ResponseStatus.CREATED.value, body)
