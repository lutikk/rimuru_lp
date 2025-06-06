import time

from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message

bl = UserLabeler()

bl.vbml_ignore_case = True


async def get_ping(message: Message, answer: str) -> str:
    delta = round(time.time() - message.date, 2)

    # А ты думал тут все чесно будет? Не, я так не работаю...
    if delta < 0:
        delta = "666"

    return f"{answer} Модуль ЛП\n" \
           f"Ответ через {delta} с"


@bl.message(text="<pref:service_prefix> пинг")
async def ping_wrapper(message: Message, **kwargs):
    user_db = User.load()
    if not user_db.id == message.from_id:
        return
    await edit_message(
        message,
        await get_ping(message, "ПОНГ")
    )
