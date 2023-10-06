import os
from glob import glob
from typing import Optional

from dask.base import compute
from dask.delayed import delayed
from flask import Blueprint, Response, jsonify, request
from pandas import errors as pd_errors
from pathvalidate import sanitize_filepath

from myoratio.api import API, ResponseStatus
from myoratio.api.auth import auth
from myoratio.api.helpers import PathHelper

from .imu import IMU

imu_blueprint = Blueprint("imu_blueprint", __name__)


@delayed
def parallel_imu_processing(body: dict, participant: str) -> Optional[dict]:
    data_path_parameter = os.path.normpath(body["data_path"])

    data_path = os.path.join(
        PathHelper.get_analysis_folder_path(data_path_parameter, body["analysis"]),
        participant,
    )

    csv_files = glob(os.path.join(data_path, "*.csv"))

    if len(csv_files) > 0:
        for csv_file in csv_files:
            csv_filename, _ = os.path.basename(csv_file).rsplit(".", 1)

            files = os.listdir(
                sanitize_filepath(
                    os.path.join(
                        PathHelper.get_metadata_analysis_path(
                            data_path_parameter, body["analysis"]
                        ),
                        participant,
                    )
                )
            )

            if f"small_angle_{csv_filename}.json" not in files or body["override"]:
                imu = None
                try:
                    imu = IMU(
                        data_path_parameter, csv_file, body["analysis"], body["config"]
                    )
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
                except Exception as error:
                    return {
                        "code": 500,
                        "status": "failed",
                        "payload": {
                            "message": f"Error occurs while trying to process IMU data. Related file: "
                            f"{imu.get_csv_path()[1]}",
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


@imu_blueprint.route("/imu/", methods=["POST"])
@auth.login_required
def generate_imu_analysis() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, "Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {
            "data_path": str,
            "analysis": str,
            "participants": [str],
            "override": bool,
            "config": {
                "id": str,
                "label": str,
                "stages": {
                    "concentric": {"label": str, "opening": bool},
                    "eccentric": {"label": str, "opening": bool},
                },
                "muscles": {"antagonist": str, "agonist": str, "angle": str},
                "is_angle_advanced": bool,
            },
        }

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                400, "Request body is not properly formatted", validation
            )

        participants = []

        for participant in body["participants"]:
            # deepcode ignore XSS: already sanitized
            participants.append(parallel_imu_processing(body, participant))

        outputs = compute(participants)

        for i in range(len(outputs[0])):
            output = outputs[0][i]

            if output is not None:
                return jsonify(output), output["code"]

        body = {
            "data_path": body["data_path"],
            "analysis": body["analysis"],
            "participants": body["participants"],
            "override": body["override"],
            "config": body["config"],
        }

        # deepcode ignore XSS: already sanitized
        return API.success_response(201, ResponseStatus.CREATED.value, body)
