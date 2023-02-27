import os

from flask import Blueprint, Response, request

from emgtrigno.api import API, ResponseStatus
from emgtrigno.api.auth import auth

from .report import Report

report_blueprint = Blueprint("report_blueprint", __name__)


@report_blueprint.route("/report/", methods=["POST"])
@auth.login_required
def generate_report() -> tuple[Response, int]:
    body = request.json

    if body is None:
        return API.error_response(
            400, f"Request body is not properly formatted", "request body is empty"
        )

    else:
        schema = {"data_path": str, "analysis": str}

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            return API.error_response(
                400, f"Request body is not properly formatted", validation
            )

        try:
            report = Report(body["data_path"], body["analysis"])
            report.generate_PDF_report()
        except Exception as error:
            return API.error_response(
                500, f"Error occurs while trying to generate PDF report", str(error)
            )

        # file deepcode ignore XSS: already sanitized
        return API.success_response(
            201,
            ResponseStatus.CREATED.value,
            {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
            },
        )
