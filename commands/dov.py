import vk_api
from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message, search_user_ids

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(text=["<pref:service_prefix> +дов", '<pref:service_prefix> +дов <users>'])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])

    if user_ids[0] in user.dov:
        await edit_message(message, "✅ Пользователь уже есть в доверенных")
        return
    user.dov.append(user_ids[0])
    user.save()
    await edit_message(message, "✅ Пользователь добавлен в доверенные ")


@bl.message(text=["<pref:service_prefix> -дов", "<pref:service_prefix> -дов <users>"])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])

    user.dov.remove(user_ids[0])
    user.save()
    await edit_message(message, "✅ Пользователь удален из игнора ")


@bl.message(text="<pref:service_prefix> довы")
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    text = "Вы доверяете:\n"
    users = await message.ctx_api.users.get(user_ids=user.dov)
    for i in users:
        name = f'[id{i.id}|{i.first_name} {i.last_name}]'
        text += f'{name}\n'
    await edit_message(message, text)


@bl.message(text="<pref:service_prefix> дов <pref_>")
async def ping_wrapper(message: Message, pref_: str):
    user = User.load()
    if not user.id == message.from_id:
        return
    user.dov_pref = pref_
    user.save()
    await edit_message(message, f'Префикс изменен на <<{pref_}>>')
