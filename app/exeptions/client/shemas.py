from pydantic import BaseModel


class BaseExceptionScheme(BaseModel):
    status: str = "Error"
    code: int
    message: str


class TokenExeptionScheme(BaseExceptionScheme):
    pass


class AuthExceptionScheme(BaseExceptionScheme):
    pass


class RequestValidationScheme(BaseExceptionScheme):
    pass
