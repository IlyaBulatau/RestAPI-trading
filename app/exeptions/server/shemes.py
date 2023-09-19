from pydantic import BaseModel


class ServerExceptionSchemes(BaseModel):
    status: str = "Server Error"
    code: int = 500
    message: str