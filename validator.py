import typing

from vbml.patcher import Patcher

from models import User

patcher = Patcher()


@patcher.validator('service_prefix')
def service_prefix(value: str) -> typing.Optional[typing.Any]:
    db = User.load()
    if f'{value.lower()} ' in db.serv_pref:
        return value


@patcher.validator('self_prefix')
def self_prefix(value: str):
    db = User.load()
    if value.lower() in db.my_pref:
        return value


@patcher.validator('alias')
def alias(value: str):
    db = User.load()
    for alias_ in db.alias:
        if value.lower() == alias_.sokr_cmd:
            return alias_
