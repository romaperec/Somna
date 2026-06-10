from app.core.exceptions import AppBaseException


class AuthBaseException(AppBaseException):
    pass

class InvalidTokenException(AuthBaseException):
    message = "Token invalid or expired."
    status_code = 401

class TokenExpiredException(AuthBaseException):
    message = "Token has expired."
    status_code = 403

class MissingTokenException(AuthBaseException):
    message = "Authentication token is missing."
    status_code = 401

class AuthenticationFailedException(AuthBaseException):
    message = "Incorrect email/username or password."
    status_code = 401

class SessionExpiredException(AuthBaseException):
    message = "Your session is expired. Please log in again."
    status_code = 401

class DatabaseException(AuthBaseException):
    message = "Internal authentication service error."
    status_code = 500

