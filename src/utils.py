from http.cookies import SimpleCookie
from pathlib import Path

from src.schemes import Cookies


def convert_cookie(cookie: str) -> dict[str, str]:
    """
    The function converts cookies from str to dict
    :param cookie: Line containing account data
    """

    _cookie = SimpleCookie()
    _cookie.load(cookie)
    cookies = {}

    for key, morsel in _cookie.items():
        cookies[key] = morsel.value

    return cookies


async def get_cookies(folder: Path = None) -> list[Cookies]:
    """
    Creates a Cookies object from .cookie files
    :param folder: Path to the folder where the .cookie files are located
    :return: List of activision accounts
    """

    files = list(folder.glob("*.cookie"))
    cookies = list()

    for file in files:
        cookies.append(
            Cookies(
                file_path=file,
                value=convert_cookie(file.read_text("utf-8")),
            )
        )

    return cookies



