import os
from glob import glob
from typing import Optional

from dask.base import compute
from dask.delayed import delayed
from flask import Blueprint, Response, request
from pandas import errors as pd_errors

from myoratio.angles import Angles
from myoratio.api import API, ResponseStatus
from myoratio.api.auth import auth
from myoratio.api.helpers import PathHelper
from myoratio.areas import Areas
from myoratio.results import Results

results_blueprint = Blueprint("results_blueprint", __name__)


@delayed
def parallel_results_processing(body: dict, participant: str) -> Optional[dict]:
    data_path_parameter = os.path.normpath(body["data_path"])

    data_path = os.path.join(
        PathHelper.get_metadata_analysis_path(data_path_parameter, body["analysis"]),
        participant,
    )

    csv_files = glob(os.path.join(data_path, f'envelope_{body["stage"]}_*.csv'))

    if len(csv_files) > 0:
        try:
            areas = Areas(data_path, body["stage"], csv_files=csv_files)
        except pd_errors.ParserError as error:
            return {
                "code": 500,
                "message": f"Error occurs while trying to read CSV files",
                "details": str(error),
            }

        try:
            areas = areas.start_processing()
            results = Results(areas, body["analysis"])

            try:
                angles = Angles(data_path)

                csv_files = glob(
                    os.path.join(data_path, f'normalized_angle_{body["stage"]}_*.csv')
                )

                if len(csv_files) > 0:
                    angles.start_processing(csv_files, body["stage"])
                else:
                    return {
                        "code": 404,
                        "message": "Missing data",
                        "details": f"No CSV files found in path: {data_path}",
                    }

            except Exception as error:
                return {
                    "code": 500,
                    "message": f"Error occurs while trying to compute mean angles",
                    "details": str(error),
                }

            try:
                ratios = results.compute_ratios(body["stage"])
            except Exception as error:
                return {
                    "code": 500,
                    "message": f"Error occurs while trying to compute ratios",
                    "details": str(error),
                }

            results.write_ratios(data_path, body["stage"], ratios)

        except Exception as error:
            return {
                "code": 500,
                "message": f"Error occurs while trying to process areas",
                "details": str(error),
            }

    else:
        return {
            "code": 404,
            "message": "Missing data",
            "details": f"No CSV files found in path: {data_path}",
        }


@results_blueprint.route("/results/", methods=["POST"])
@auth.login_required
def generate_results() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, f"Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {"data_path": str, "analysis": str, "stage": str, "participants": [str]}

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                400, f"Request body is not properly formatted", validation
            )

        participants = []

        for participant in body["participants"]:
            # deepcode ignore XSS: already sanitized
            participants.append(parallel_results_processing(body, participant))

        outputs = compute(participants)

        for i in range(len(outputs[0])):
            output = outputs[0][i]

            if output is not None:
                # deepcode ignore XSS: already sanitized
                return API.error_response(
                    output["code"], output["message"], output["details"]
                )

        # deepcode ignore XSS: already sanitized
        return API.success_response(
            201,
            ResponseStatus.CREATED.value,
            {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "stage": body["stage"],
                "participants": body["participants"],
            },
        )
