from dataclasses import dataclass
from pathlib import Path

from environs import Env

# https://github.com/Latand/tgbot_template_v3/blob/master/tgbot/config.py


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: set[int]

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = set(map(int, env.list("ADMINS")))

        return TgBot(token=token, admin_ids=admin_ids)


@dataclass
class Script:
    """
    Creates the Script object from environment variables.
    """

    sleep_time: float
    concurrent_requests: int

    @staticmethod
    def from_env(env: Env):
        """
        Creates the Script object from environment variables.
        """

        sleep_time = env.float("SLEEP_TIME")
        concurrent_requests = env.int("CONCURRENT_REQUESTS")

        return Script(
            sleep_time=sleep_time,
            concurrent_requests=concurrent_requests,
        )


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point
    of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    script : Script
        Holds the settings related to the main script.
    """

    tg_bot: TgBot
    script: Script


def load_config(path: str | Path = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process
    environment.

    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        script=Script.from_env(env),
    )
