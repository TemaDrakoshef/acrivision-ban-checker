import asyncio
import sys
from pathlib import Path

import httpx
import loguru

from src import activision, utils, telegram
from src.config import load_config, Config
from src.schemes import Cookies, BanTypes


def setup_logging():
    """
    The function configures logging in the project
    """
    loguru.logger.remove()
    loguru.logger.add(
        sys.stdout,
        format="<lvl>[</lvl><c>{time:HH:mm:ss.SSS}</c><lvl>]</lvl> "
               "<lvl>—</lvl> <lvl>{message}</lvl>",
    )

    loguru.logger.opt(colors=True).info("Starting script")


async def check_account(client: httpx.AsyncClient, config: Config, cookie: Cookies):
    """
    The function checks the activision account for lockouts
    :param config: The object that stores all the data from the .env file
    :param client: Asynchronous HTTP client object
    :param cookie: Object required for authorization in activision account
    """

    profile = await activision.get_profile(client, cookie)
    status = await activision.get_status(client, cookie)

    logger_activision = "Activision - {username} - {message}"
    activision_level = "INFO"
    logger_activision_message = ""

    if profile is None or status is None:
        return loguru.logger.opt(colors=True).error(
            logger_activision.format(
                username=cookie.file_path.name,
                message="Failed to retrieve account data",
            )
        )

    text = (
        f"👤 {profile.username}\n"
    )

    if not status.bans:
        text = text + "✅ There are no bans\n"

        activision_level = "SUCCESS"
        logger_activision_message = "There are no bans"
    else:
        match status.bans[0].enforcement:
            case BanTypes.permanent:
                text = text + "💀 Permanent ban\n"

                activision_level = "ERROR"
                logger_activision_message = "Permanent ban"
            case BanTypes.under_review:
                text = text + "👻 Shadow ban\n"

                loguru.logger.opt(colors=True).warning(
                    logger_activision.format(
                        username=profile.username,
                        message="Shadow ban",
                    )
                )

                activision_level = "WARNING"
                logger_activision_message = "Shadow ban"

    loguru.logger.opt(colors=True).log(
        activision_level,
        logger_activision.format(
            username=profile.username,
            message=logger_activision_message,
        )
    )

    for admin_id in config.tg_bot.admin_ids:
        response = await telegram.send_message(
            client,
            bot_token=config.tg_bot.token,
            user_id=admin_id,
            text=text,
        )

        if not response["ok"]:
            loguru.logger.opt(colors=True).warning(
                f"Telegram - {profile.username} - "
                f"{admin_id}: <c>{response['description']}</c>"
            )


def divide_list(lst: list, n: int) -> list[list]:
    """
    The function divides the list into x number of parts with n elements in each part
    :param lst: The list that needs to be shared
    :param n: Number of items in one list
    :return: Split the list. If the list contains insufficient If the list contains
        insufficient number of items to split, the original list will be returned
    """

    if len(lst) < n:
        return [lst]
    else:
        divided_list = list()
        for i in range(0, len(lst), n):
            divided_list.append(lst[i:i + n])

        return divided_list


async def main():
    """
    The function simultaneously runs n number of functions
    to check activision accounts for bans
    """
    setup_logging()

    config = load_config(Path(".env"))
    client = httpx.AsyncClient(timeout=120)

    accounts = await utils.get_cookies(Path("cookies"))
    cookies_list = divide_list(
        lst=accounts,
        n=config.script.concurrent_requests,
    )

    loguru.logger.opt(colors=True).info(
        f"Received <g>{len(accounts)}</g> cookie files"
    )

    while True:
        for cookies in cookies_list:
            tasks = list()

            for cookie in cookies:
                tasks.append(
                    asyncio.create_task(check_account(client, config, cookie))
                )

            await asyncio.gather(*tasks)

        loguru.logger.opt(colors=True).info(
            f"Falling asleep for {config.script.sleep_time} seconds"
        )

        await asyncio.sleep(config.script.sleep_time)


if __name__ == '__main__':
    asyncio.run(main())
