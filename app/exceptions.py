from fastapi import HTTPException, status


class ServerErrorException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server Error"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class KeynotFound(ServerErrorException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Key doesn't exist"


class KeyAlreadyExists(ServerErrorException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Key already exists"
