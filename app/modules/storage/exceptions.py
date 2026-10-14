from app.core.exceptions import AppBaseException


class StorageBaseException(AppBaseException): ...


class InvalidFileTypeException(StorageBaseException):
    message = "Unsupported media type."
    status_code = 415


class FileNotFoundException(StorageBaseException):
    message = "File not found."
    status_code = 404


class PermissionDeniedException(StorageBaseException):
    message = "You are not the owner of this file."
    status_code = 403


class FileTooLargeException(StorageBaseException):
    message = "File exceeds maximum allowed size."
    status_code = 413