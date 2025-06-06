
from typing import Optional

import vk_api
from vkbottle.user import Message, UserLabeler

from models import User, Alias
from utils import edit_message, send_request

bl = UserLabeler()

bl.vbml_ignore_case = True


async def send_signal(
        database: User,
        message: Message,
        alias: Alias,
        separator: str = ' ',
        signal: Optional[str] = None
):
    vk = vk_api.VkApi(token=database.token)
    _message_ = vk.method("messages.getByConversationMessageId",
                          {"conversation_message_ids": message.conversation_message_id,
                           'peer_id': message.peer_id})
    message_ = _message_['items'][0]
    prepared_text = alias.poln_cmd
    prepared_text += f"{separator}{signal}" if signal else ''

    __model = {
        "user_id": message_['from_id'],
        "method": "lpSendMySignal",
        "secret": database.secret_code,
        "message": {
            "conversation_message_id": message_['conversation_message_id'],
            "from_id": message_['from_id'],
            "date": message.date,
            "text": prepared_text,
            "peer_id": message.peer_id
        },
        "object": {
            "chat": None,
            "from_id": message_['from_id'],
            "value": prepared_text,
            "conversation_message_id": message_['conversation_message_id']
        },

    }

    await send_request(__model, message)


@bl.message(text="<pref:service_prefix> +алиас <name>\n<sok_cmd>\n<cmd>")
async def ping_wrapper(message: Message, name: str, sok_cmd: str, cmd: str, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    alias = Alias(
        name=name,
        sokr_cmd=sok_cmd,
        poln_cmd=cmd
    )
    for i in user.alias:
        if i.name == name:
            await edit_message(message, "Такой алиас уже существует")
            return
    user.alias.append(alias)
    user.save()
    await edit_message(message, f"Создал алиас <<{name}>>")


@bl.message(text="<pref:service_prefix> -алиас <name>")
async def ping_wrapper(message: Message, name: str, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    for i in user.alias:
        if i.name == name:
            user.alias.remove(i)
            user.save()
            await edit_message(message, f"Алиас <<{i.name}>> удален")
            return
    await edit_message(message, f'Алиас <<{name}>> не найден')


@bl.message(text="<pref:service_prefix> алиасы")
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    sq = 0
    text = "📃 Ваши алиасы:\n"
    for i in user.alias:
        sq += 1
        text += f'{sq}. {i.name} ({i.sokr_cmd} -> .л {i.poln_cmd})\n'
    await edit_message(message, text)


@bl.message(text=['<alias:alias> <signal>', '<alias:alias>'])
async def duty_signal(message: Message, alias: Alias, signal: str = None):
    db = User.load()
    if not db.id == message.from_id:
        return
    await send_signal(db, message, alias, ' ', signal)


@bl.message(text='<alias:alias>\n<signal>')
async def duty_signal_new_line(message: Message, alias: Alias, signal: str):
    db = User.load()
    if not db.id == message.from_id:
        return
    await send_signal(db, message, alias, '\n', signal)
