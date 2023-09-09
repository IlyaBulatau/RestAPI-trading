from app.utils.helpers import generate_link_info_for_response_model
from app.schemas.responses import LinkResponse
from app.settings.constance import USER_ROUTE_URI, AUTH_ROUTE_URI


def links_to_auth_process() -> list[LinkResponse]:
    """
    create a list of links consisting of ListResponse schema
    Used as dependency in signUp handler
    """
    links = [
        generate_link_info_for_response_model(
            title="SignIn",
            route=AUTH_ROUTE_URI + "/signin",
            desc="Path to SignIn processe",
        ),
    ]
    return links


def link_user_response(username: str = "{username}") -> list[LinkResponse]:
    """
    create a list of links consisting of ListResponse schem
    Used for added payload each user to response in get_user handler
    """
    links = [
        generate_link_info_for_response_model(
            title="User profile",
            route=USER_ROUTE_URI + "/" + username,
            desc=f"Path to {username} profile",
        ),
        generate_link_info_for_response_model(
            title="My profile", route=USER_ROUTE_URI + "/me", desc="Show my profle"
        ),
        generate_link_info_for_response_model(
            title="Get all users",
            route=USER_ROUTE_URI,
            desc="Get all users with params, limit and offset",
        ),
    ]

    return links
