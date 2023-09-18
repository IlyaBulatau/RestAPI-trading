from pydantic import BaseModel, ConfigDict


class BaseExceptionScheme(BaseModel):
    status: str = "Error"
    code: int
    message: str


class TokenExeptionScheme(BaseExceptionScheme):
    pass


class AuthExceptionScheme(BaseExceptionScheme):
    pass