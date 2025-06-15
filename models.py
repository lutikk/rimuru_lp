import json
import os

from pydantic import BaseModel


class UserIdLp(BaseModel):
    user_id: int
    key: str


class Alias(BaseModel):
    name: str
    sokr_cmd: str
    poln_cmd: str


class IgnoreUser(BaseModel):
    user_id: int
    peer_id: int


class HelloChat(BaseModel):
    peer_id: int
    hello_text: str


class User(BaseModel):
    id: int
    token: str
    my_pref: list = ['.л', '!л']
    serv_pref: list = ['.слп ', '!слп ']
    time_commands: float = 8000
    alias: list[Alias] = []
    dov: list[int] = []
    dov_pref: str = '..'
    secret_code: str = 'Noy'
    global_ignore: list[int] = []
    ignore: list[IgnoreUser] = []
    hello: list[HelloChat] = []

    @staticmethod
    def get_path() -> str:
        return os.path.join(os.getcwd(), 'config.json')

    def save(self):
        path_to_file = User.get_path()
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                self.model_dump_json(indent=2)  # Исправлено здесь
            )

    @staticmethod
    def load() -> 'User':
        path_to_file = User.get_path()
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                data = file.read()
                if not data:  # Проверка на пустой файл
                    raise json.JSONDecodeError("Empty file", "", 0)
                db = User(**json.loads(data))
        except (FileNotFoundError, json.JSONDecodeError):
            from utils import get_token
            token_input = input("Файл конфигурации не найден. Пожалуйста, введите токен: ")
            token = get_token(token_input)

            db = User(id=token['user_id'], token=token['token'])
            db.save()

        return db


class UserIdLpSave(User):
    key: str