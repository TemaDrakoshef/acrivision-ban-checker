from httpx import AsyncClient

BASE_URL = "https://api.telegram.org/bot{token}"


async def send_message(
        client: AsyncClient,
        bot_token: str,
        user_id: int,
        text: str,
):
    """
    The function sends a message to a specific user in Telegram
    :param client: Asynchronous HTTP client object
    :param bot_token: A unique token that represents the identifier of
        your bot in the Telegram API
    :param user_id: ID of the user to whom the message will be sent
    :param text: Text message to be sent to the user with the given user_id
    :return: An object representing the message sent
    """

    url = BASE_URL + "/sendMessage"
    payload = {
        "chat_id": user_id,
        "text": text,
    }

    try:
        response = await client.request(
            "POST",
            url=url.format(token=bot_token),
            data=payload,
        )

        return response.json()
    except Exception as _ex:
        print("Произошла ошибка при отправке уведомления")
