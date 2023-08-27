from app.exeptions.http.shemas import Desciption, UserEmailNotFoundResponse
from app.exeptions.http.response_text import TEXT_EMAIL_IS_EXISTS, TITLE_EMAIL_EXEPTION


class ResponseGenerator:
    ...


def generate_response_for_email_exeption(email: str, status_code: int):
    """
    generate json response for handler exeption
    """
    detail_schema = dict(Desciption(field="email",
                                    text=TEXT_EMAIL_IS_EXISTS.format(email=email)))

    return dict(UserEmailNotFoundResponse(
        title=TITLE_EMAIL_EXEPTION,
        status=status_code,
        detail=detail_schema
    ))