from typing import Optional

from dask.base import compute
from dask.delayed import delayed
from flask import Blueprint, Response, request

from myoratio.api import API, ResponseStatus
from myoratio.api.auth import auth
from myoratio.api.helpers import JSONHelper, PathHelper

from .report import Report
from .summary import Summary

report_blueprint = Blueprint("report_blueprint", __name__)


@delayed
def parallel_xlsx_report_generator(
    body: dict, participant: tuple[str, dict]
) -> Optional[dict]:
    try:
        report = Report(
            body["data_path"],
            body["analysis"],
            body["stage"],
            body["config"],
            participant,
        )
        report.generate_XLSX_report()
    except Exception as error:
        return {
            "code": 500,
            "message": "Error occurs while trying to generate XLSX report",
            "details": str(error),
        }


@report_blueprint.route("/report/xlsx", methods=["POST"])
@auth.login_required
def generate_xlsx_report() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, "Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {
            "data_path": str,
            "analysis": str,
            "stage": str,
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


@report_blueprint.route("/summary", methods=["POST"])
@auth.login_required
def generate_xlsx_summary() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, "Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {
            "data_path": str,
            "analysis": str,
            "stage": str,
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

        try:
            summary = Summary(
                body["data_path"], body["analysis"], body["stage"], body["config"]
            )
            summary.generate_XLSX_summary()
        except Exception as error:
            return API.error_response(
                500, "Error occurs while trying to generate XLSX summary", str(error)
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
