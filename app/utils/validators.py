import re


def username_validate(username: str) -> str:
    result = re.match(r"^[a-zA-Z0-9]+([_ -]?[a-zA-Z0-9])*$", username)
    if not result:
        raise ValueError("Username must be a word or set of words separated by 1 space or underscore")
    return username

def password_validate(password: str) -> str:
    result = re.match(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', password)
    if not result:
        raise ValueError("the Password must be more than 8 characters long and contain letters of the English alphabet numbers and special characters")
    return password

