class SpbBaseException(Exception):
    HTTP_CODE = 400

    def __init__(self, message: str) -> None:
        self.message = message


class ResourceNotFound(SpbBaseException):
    HTTP_CODE = 404
