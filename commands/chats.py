from vkbottle.user import Message, UserLabeler, rules

from models import User, HelloChat
from utils import edit_message

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.chat_message(rules.ChatActionRule(["chat_invite_user", "chat_invite_user_by_link"]))
async def chat_invite_user(message: Message, **kwargs):
    user = User.load()
    for i in user.hello:
        if i.peer_id == message.peer_id:
            await message.ctx_api.messages.send(
                peer_id=i.peer_id,
                message=i.hello_text,
                random_id=0
            )
            return


@bl.message(text=[
    "<pref:service_prefix> +приветствие\n<text>",
    "<pref:service_prefix> +приветствие \n<text>"

])
async def add_hello(message: Message, text: str, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    for i in user.hello:
        if i.peer_id == message.peer_id:
            await edit_message(message, "В этом чате уже установлено приветствие")
            return
    hello = HelloChat(
        peer_id=message.peer_id,
        hello_text=text
    )
    user.hello.append(hello)
    user.save()
    await edit_message(message, "Добавлено приветствие в этот чат")


@bl.message(text="<pref:service_prefix> -приветствие")
async def del_hello(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    for i in user.hello:
        if i.peer_id == message.peer_id:
            user.hello.remove(i)
            user.save()
            await edit_message(message, "Удалил приветствие")
            return

    await edit_message(message, "Приветствие не найдено")
