import vk_api
from vkbottle.user import Message, UserLabeler

from models import User, IgnoreUser
from utils import edit_message, search_user_ids

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(text=["<pref:service_prefix> +игнор", '<pref:service_prefix> +игнор <users>'])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])
    ignore = IgnoreUser(
        user_id=user_ids[0],
        peer_id=message.peer_id
    )
    for i in user.ignore:
        if i.peer_id == message.peer_id and i.user_id == user_ids[0]:
            await edit_message(message, "✅ Этот пользователь уже в игноре")
            return
    user.ignore.append(ignore)
    user.save()
    await edit_message(message, "✅ Пользователь добавлен в игнор ")


@bl.message(text=["<pref:service_prefix> -игнор", "<pref:service_prefix> -игнор <users>"])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])
    ignore = IgnoreUser(
        user_id=user_ids[0],
        peer_id=message.peer_id
    )
    user.ignore.remove(ignore)
    user.save()
    await edit_message(message, "✅ Пользователь удален из игнора ")


@bl.message(text=["<pref:service_prefix> +глоигнор", "<pref:service_prefix> +глоигнор <user>"])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])
    if user_ids[0] in user.global_ignore:
        await edit_message(message, "✅ Пользователь уже в глоигноре")
        return

    user.global_ignore.append(user_ids[0])
    user.save()
    await edit_message(message, "✅ Пользователь добавлен в глоигнор ")


@bl.message(text=["<pref:service_prefix>-глоигнор", '<pref:service_prefix> -глоигнор <users>'])
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    vk = vk_api.VkApi(token=user.token)
    message_ = vk.method("messages.getByConversationMessageId",
                         {"conversation_message_ids": message.conversation_message_id,
                          'peer_id': message.peer_id})
    user_ids = search_user_ids(message_['items'][0])

    user.global_ignore.remove(user_ids[0])
    user.save()
    await edit_message(message, "✅ Пользователь удален из глоигнора")


@bl.message(text="<pref:service_prefix> игнор лист")
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    text = "В этом чате вы игнорируете:\n"
    for i in user.ignore:
        if i.peer_id == message.peer_id:
            a = await message.get_user(user_ids=i.user_id)
            name = f'[id{a.id}|{a.first_name} {a.last_name}]'
            text += f'{name}\n'
    await edit_message(message, text)


@bl.message(text="<pref:service_prefix> глоигнор лист")
async def ping_wrapper(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    users = await message.ctx_api.users.get(user_ids=user.global_ignore)

    text = "Вы игнорируете:\n"
    for a in users:
        name = f'[id{a.id}|{a.first_name} {a.last_name}]'
        text += f'{name}\n'
    await edit_message(message, text)
