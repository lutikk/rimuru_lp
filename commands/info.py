import os

import psutil
import requests
from vkbottle.user import Message, UserLabeler

from models import User
from utils import edit_message

bl = UserLabeler()

bl.vbml_ignore_case = True


def pid_cpu_usage(pid: int) -> float:
    process = psutil.Process(pid)
    cpu_percent = process.cpu_percent()
    cpu_count = psutil.cpu_count()
    return cpu_percent / cpu_count


@bl.message(text="<pref:service_prefix> инфо")
async def info(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    process = psutil.Process()
    mem_usage = process.memory_info().rss
    mem_usage_mb = mem_usage / 1024 / 1024
    version = f'4.4.3'
    text = f'RimuruLP v{version}\n'
    text += f'Мои префиксы: {" ".join(user.my_pref) if user.my_pref else ""}\n' \
            f'Сервисные префиксы: {"".join(user.serv_pref) if user.serv_pref else ""}\n' \
            f'Алиасы: {len(user.alias)}\n' \
            f'Доверенных: {len(user.dov)}\n' \
            f'Повторялка: {user.dov_pref}\n' \
            f'Игнорируем: {len(user.ignore)}\n' \
            f'Глобально игнорируем: {len(user.global_ignore)}\n' \
            f'Приветствия: {len(user.hello)}\n' \
            f'LP Memory: {round(mem_usage_mb, 2)} Мб\n\n'
    version_server = requests.get('https://api.rimuruproject.ru/lp/version/')
    version_server_json = version_server.json()
    if version != version_server_json['version']:
        text += f"Вышла новая версия LP {version_server_json['version']}"
    await edit_message(message, text)


@bl.message(text="<pref:service_prefix> сервер")
async def info(message: Message, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    process = psutil.Process()
    mem_usage = process.memory_info().rss
    mem_usage_mb = mem_usage / 1024 / 1024
    pid = os.getpid()
    await edit_message(message, f"LP Memory: {round(mem_usage_mb, 2)} Мб\n"
                                f"LP CPU: {round(pid_cpu_usage(pid))}")


@bl.message(text="<pref:service_prefix> +преф <sq>")
async def info(message: Message, sq: str, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    if sq.lower() in user.my_pref:
        await edit_message(message, f"У вас уже есть префикс <<{sq.lower()}>>")
        return
    user.my_pref.append(sq.lower())
    user.save()
    await edit_message(message, f"Префикс <<{sq.lower()}>> добавлен")
    return


@bl.message(text="<pref:service_prefix> -преф <sq>")
async def info(message: Message, sq: str, **kwargs):
    user = User.load()
    if not user.id == message.from_id:
        return
    if not sq.lower() in user.my_pref:
        await edit_message(message, f"У вас нет префикса <<{sq.lower()}>>")
        return
    user.my_pref.remove(sq.lower())
    user.save()
    await edit_message(message, f"Префикс <<{sq.lower()}>> удален")
    return
