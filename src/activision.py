from httpx import AsyncClient

from src.schemes import Cookies, Profile, Status

BASE_URL = "https://support.activision.com"


async def get_status(client: AsyncClient, cookie: Cookies) -> Status:
    """
    The function retrieves the current status of the activision account
    :param client: Asynchronous HTTP client object
    :param cookie: Object required for authorization in activision account
    :return: Object containing activision account status data
    """

    url = BASE_URL + "/api/bans/appeal"

    try:
        response = await client.request("GET", url, cookies=cookie.value)

        return Status(
            **response.json(),
        )
    except Exception as _ex:
        pass


async def get_profile(client: AsyncClient, cookie: Cookies) -> Profile:
    """
    The function retrieves all activision account data
    :param client: Asynchronous HTTP client object
    :param cookie: Object required for authorization in activision account
    :return: Object containing basic user data
    """

    url = BASE_URL + "/api/profile"
    try:
        response = await client.request("GET", url, cookies=cookie.value)

        return Profile(
            **response.json(),
            cookies=cookie,
        )
    except Exception as _ex:
        pass
