class AppBaseException(Exception):
    message: str = "An unexpected exception occurred."

    def __init__(self, message: str) -> None:
        if message:
            self.message = message
        super().__init__(self.message)
