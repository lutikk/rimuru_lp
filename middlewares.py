from vkbottle import BaseMiddleware
from vkbottle.user import Message

from models import User


class UserIgnore(BaseMiddleware[Message]):

    async def pre(self):
        user_db = User.load()
        user_id = user_db.id
        if self.event.from_id < 0:
            self.stop("Боты нам не нужны")
        if int(user_id) == self.event.from_id:
            return

        if self.event.from_id in user_db.dov and self.event.text.lower().split()[0] == user_db.dov_pref:
            new_text = self.event.text.split(maxsplit=1)[1]
            await self.event.answer(new_text)
            self.stop("Юзер в дове не трать мощности")

        if self.event.from_id in user_db.global_ignore and self.event != int(user_id):
            await self.event.ctx_api.request("messages.delete",
                                             {"peer_id": self.event.peer_id, "message_id": self.event.id})
            self.stop("Юзер в игноре не трать мощности")

        for i in user_db.ignore:
            if i.user_id == self.event.from_id and i.peer_id == self.event.peer_id and self.event != int(user_id):
                await self.event.ctx_api.request("messages.delete",
                                                 {"peer_id": self.event.peer_id, "message_id": self.event.id})
                self.stop("Юзер в игноре не трать мощности")
