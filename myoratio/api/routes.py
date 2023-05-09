from flask import Blueprint, Response, request

from .api import API, ResponseStatus

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/ping/", methods=["GET"])
def ping() -> tuple[Response, int]:
    return API.success_response(200, ResponseStatus.OK.value, {"message": "API started"})
