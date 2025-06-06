import re
import urllib.parse

import aiohttp
import requests as req
import vk_api
from vk_api import VkApi
from vkbottle.user import Message

from lp import GET_LP_INFO_LINK, CALLBACK_LINK
from models import User



async def edit_message(
        message: Message,
        text: str = '',
        att: str = ''
):
    return await message.ctx_api.messages.edit(peer_id=message.peer_id, message=text,
                                               message_id=message.id, keep_forward_messages=True,
                                               keep_snippets=True,
                                               dont_parse_links=False,
                                               attachment=att

                                               )


def get_code(token: str):
    sq = req.get(url=GET_LP_INFO_LINK(), json={'token': token}, verify=False)
    print(sq.json())
    return sq.json()['secret_code']


def get_token(url: str):
    try:
        fragment = url.split('#')[-1]

        params = urllib.parse.parse_qs(fragment)

        access_token = params.get('access_token', [None])[0]
        user_id = params.get('user_id', [None])[0]

        return {
            "token": access_token,
            "user_id": user_id
        }
    except:
        user_id = VkApi(token=url).method("users.get")[0]['id']
        return {
            "token": url,
            "user_id": user_id
        }


def get_user_id_by_domain(user_domain: str):
    """Поиск ID по домену"""
    user = User.load()
    vk = vk_api.VkApi(token=user.token)

    obj = vk.method('utils.resolveScreenName', {"screen_name": user_domain})

    if isinstance(obj, list):
        return
    if obj['type'] == 'user':
        return obj["object_id"]


def search_user_ids(e):
    result = []
    if e['text']:
        regex = r"(?:vk\.com\/(?P<user>[\w\.]+))|(?:\[id(?P<user_id>[\d]+)\|)"

        for user_domain, user_id in re.findall(regex, e['text']):
            if user_domain:
                result.append(get_user_id_by_domain(user_domain))
            if user_id:
                result.append(int(user_id))

    if e.get('reply_message') and e.get('reply_message').get('from_id') > 0:
        result.append(e.get('reply_message').get('from_id'))

    if e.get('fwd_messages'):
        for msg in e.get('fwd_messages'):
            if msg['from_id'] > 0:
                result.append(msg['from_id'])
    _result = []
    for r in result:
        if r is not None:
            _result.append(r)
    return _result


async def send_request(request_data: dict, mes: Message):
    message = ""
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.post(CALLBACK_LINK(), json=request_data) as resp:
            if resp.status != 200:
                message = f"⚠ Ошибка сервера Rimulu. Сервер, ответил кодом {resp.status}."
            else:
                data_json = await resp.json()
                if data_json['response'] == 'ok':
                    return
                elif data_json['response'] == "error":
                    if data_json.get('error_code') == 1:
                        message = f"⚠ Ошибка сервера Rimulu. Сервер, ответил: <<Пустой запрос>>"
                    elif data_json.get('error_code') == 2:
                        message = f"⚠ Ошибка сервера Rimulu. Сервер, ответил: <<Неизвестный тип сигнала>>"
                    elif data_json.get('error_code') == 3:
                        message = (
                            f"⚠ Ошибка сервера Rimulu. "
                            f"Сервер, ответил: <<Пара пользователь/секрет не найдены>>"
                        )
                    elif data_json.get('error_code') == 4:
                        message = f"⚠ Ошибка сервера Rimulu. Сервер, ответил: <<Беседа не привязана>>"
                    elif data_json.get('error_code') == 10:
                        message = f"⚠ Ошибка сервера Rimulu. Сервер, ответил: <<Не удалось связать беседу>>"
                    else:
                        message = (
                            f"⚠ Ошибка сервера Rimulu. "
                            f"Сервер, ответил: <<Ошибка #{data_json.get('error_code')}>>"
                        )
                elif data_json['response'] == "vk_error":
                    message = (
                        f"⚠ Ошибка сервера Rimulu. "
                        f"Сервер, ответил: "
                        f"<<Ошибка VK {data_json.get('error_code')} {data_json.get('error_message', '')}>>"
                    )
    if message:
        await mes.ctx_api.messages.edit(peer_id=mes.peer_id, message=message,
                                        message_id=mes.id, keep_forward_messages=True,
                                        keep_snippets=True,
                                        dont_parse_links=False

                                        )
