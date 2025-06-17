from http import HTTPStatus
from typing import Any

from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(
        self,
        detail: Any = HTTPStatus.BAD_REQUEST.phrase,
    ):
        super().__init__(HTTPStatus.BAD_REQUEST.value, detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: Any = HTTPStatus.FORBIDDEN.phrase):
        super().__init__(HTTPStatus.FORBIDDEN.value, detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: Any = HTTPStatus.UNAUTHORIZED.phrase):
        super().__init__(HTTPStatus.UNAUTHORIZED.value, detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: Any = HTTPStatus.NOT_FOUND.phrase):
        super().__init__(HTTPStatus.NOT_FOUND.value, detail)


class BadGatewayException(HTTPException):
    def __init__(
        self,
        detail: Any = HTTPStatus.BAD_GATEWAY.phrase,
    ):
        super().__init__(HTTPStatus.BAD_GATEWAY.value, detail)


class GatewayTimeoutException(HTTPException):
    def __init__(
        self,
        detail: Any = HTTPStatus.GATEWAY_TIMEOUT.phrase,
    ):
        super().__init__(HTTPStatus.GATEWAY_TIMEOUT.value, detail)


class HTTPClientErrorStatusException(Exception):
    """
    The response had an error HTTP status of 4xx.

    May be raised when calling `response.raise_for_status()`
    """

    def __init__(
        self,
        status_code: int,
        response_text: Any,
    ):
        super().__init__(f"HTTP request status {status_code}")
        self.status_code = status_code
        self.response_text = response_text


class InternalServerErrorException(HTTPException):
    def __init__(
        self,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value,
        detail: Any = HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
    ):
        super().__init__(status_code, detail)
        self.status_code = status_code
        self.detail = detail
