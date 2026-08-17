from app.core.exceptions import AppBaseException


class UserBaseException(AppBaseException):
    pass


class UserEmailAlreadyExistsException(UserBaseException):
    message = "User with this email already exists."
    status_code = 409


class UserUsernameExistsException(UserBaseException):
    message = "User with this username already exists."
    status_code = 409


class UserNotFoundException(UserBaseException):
    message = "User not found."
    status_code = 404


class UserInvalidPasswordException(UserBaseException):
    message = "Password is invalid."
    status_code = 401


class UserPasswordsMatchException(UserBaseException):
    message = "The new password must not match the current one."
    status_code = 400
