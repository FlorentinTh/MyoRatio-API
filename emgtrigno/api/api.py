from enum import Enum
from typing import Optional

from flask import Response, jsonify
from simple_schema_validator import schema_validator


class ResponseStatus(Enum):
    OK = "ok"
    CREATED = "created"
    ERROR = "error"


class API:
    @staticmethod
    def error_response(code: int, message: str, details: str) -> tuple[Response, int]:
        body = {
            "code": code,
            "status": ResponseStatus.ERROR.value,
            "payload": {
                "message": message,
                "details": details,
            },
        }

        return jsonify(body), code

    @staticmethod
    def success_response(code: int, status: str, payload: dict) -> tuple[Response, int]:
        if status not in [status.value for status in ResponseStatus]:
            raise ValueError(f"Expected a value from ResponseStatus, but got {status}")

        body = {
            "code": code,
            "status": status,
            "payload": payload,
        }

        return jsonify(body), code

    @staticmethod
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
