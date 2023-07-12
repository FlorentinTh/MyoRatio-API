import os
from glob import glob

from flask import Blueprint, Response, request

from myoratio.api import API, ResponseStatus
from myoratio.api.auth import auth
from myoratio.api.helpers import PathHelper

from .points import Points

points_blueprint = Blueprint("points_blueprint", __name__)


@points_blueprint.route("/points/", methods=["POST"])
@auth.login_required
def get_points_automatically() -> tuple[Response, int]:
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
            "participant": str,
            "iteration": int,
        }

        validation = API.validate_request_body(body, schema)

        if validation is not None:
            # deepcode ignore XSS: already sanitized
            return API.error_response(
                400, "Request body is not properly formatted", validation
            )

        data_path = os.path.join(
            PathHelper.get_metadata_analysis_path(
                os.path.normpath(body["data_path"]), body["analysis"]
            ),
            body["participant"],
        )

        json_files = glob(os.path.join(data_path, "filtered_*.json"))
        points = Points(body["stage"], json_files[body["iteration"]])

        try:
            points = points.get_points()
        except Exception as error:
            return API.error_response(
                500,
                "Error occurs while trying to retrieve points automatically",
                str(error),
            )

        # deepcode ignore XSS: already sanitized
        return API.success_response(
            200,
            ResponseStatus.OK.value,
            {
                "data_path": body["data_path"],
                "analysis": body["analysis"],
                "stage": body["stage"],
                "iteration": body["iteration"],
                "participant": body["participant"],
                "points": points,
            },
        )
