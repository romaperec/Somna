from app.core.exceptions import AppBaseException


class UserBaseException(AppBaseException):
    pass


class UserEmailAlreadyExistsException(UserBaseException):
    message = "User with this email already exists."


class UserUsernameExistsException(UserBaseException):
    message = "User with this username already exists."


class UserNotFoundException(UserBaseException):
    message = "User not found."


class UserInvalidPasswordException(UserBaseException):
    message = "Password is invalid."


class UserPasswordsMatchException(UserBaseException):
    message = "The new password must not match the current one."
