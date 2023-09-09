from app.utils.helpers import generate_link_info_for_response_model
from app.schemas.responses import LinkResponse


def links_to_auth_process() -> list[LinkResponse]:
    """
    create a list of links consisting of ListResponse schema
    Used as dependency in signUp handler
    """
    links = [
        generate_link_info_for_response_model(
            title="SignIn", route="/signin", desc="Path to SignIn processe"
        ),
    ]
    return links


def links_to_get_users_process(username: str) -> list[LinkResponse]:
    """
    create a list of links consisting of ListResponse schem
    Used for added payload to response in get_user handler
    """
    links = [
        generate_link_info_for_response_model(
            title="User operations",
            route=f"/v1/api/users/{username}",
            desc=f"Path to {username} profile",
        )
    ]

    return links
