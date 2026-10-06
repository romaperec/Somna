from app.core.exceptions import AppBaseException


class StorageBaseException(AppBaseException): ...


class InvalidFileTypeException(StorageBaseException):
    message = "Unsupported media type."
    status_code = 415


class FileNotFound(StorageBaseException):
    message = "File not found."
    status_code = 404


class PermissionDenied(StorageBaseException):
    message = "You are not the owner of this file."
    status_code = 403
