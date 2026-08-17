class AppBaseException(Exception):
    message: str = "An unexpected exception occurred."
    status_code: int = 500

    def __init__(self, message: str | None = None, status_code: int | None = None):
        final_message: str = message or self.message or ""
        super().__init__(final_message)
        self.message = final_message
        if status_code:
            self.status_code = status_code
