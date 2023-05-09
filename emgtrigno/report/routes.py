from typing import Optional

from dask.base import compute
from dask.delayed import delayed
from flask import Blueprint, Response, request

from emgtrigno.api import API, ResponseStatus
from emgtrigno.api.auth import auth
from emgtrigno.api.helpers import JSONHelper, PathHelper

from .report import Report

report_blueprint = Blueprint("report_blueprint", __name__)


@delayed
def parallel_xlsx_report_generator(
    body: dict, participant: tuple[str, dict]
) -> Optional[dict]:
    try:
        report = Report(body["data_path"], body["analysis"], body["stage"], participant)

        report.generate_XLSX_report()
    except Exception as error:
        return {
            "code": 500,
            "message": f"Error occurs while trying to generate XLSX report",
            "details": str(error),
        }


@report_blueprint.route("/report/xlsx", methods=["POST"])
@auth.login_required
def generate_xlsx_report() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, f"Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {"data_path": str, "analysis": str, "stage": str}

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                400, f"Request body is not properly formatted", validation
            )

        participants = []

        metadata = JSONHelper.read_participants_metadata(
            PathHelper.get_metadata_analysis_path(body["data_path"], body["analysis"])
        )

        for participant in metadata:
            invalid = participant[1]["invalid"]
            completed = participant[1]["stages"][body["stage"]]["completed"]

            if invalid is False and completed is True:
                # deepcode ignore XSS: already sanitized
                participants.append(parallel_xlsx_report_generator(body, participant))

        outputs = compute(participants)

        for i in range(len(outputs[0])):
            output = outputs[0][i]

            if output is not None:
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
            },
        )
