from vkbottle.user import User

from commands import labelers
from middlewares import UserIgnore
from models import User as UserDB
from utils import get_code
from validator import service_prefix, self_prefix, alias

user_db = UserDB.load()

user_db.secret_code = get_code(user_db.token)
user_db.save()

bot = User(user_db.token)

bot.labeler.vbml_patcher.validator(service_prefix)
bot.labeler.vbml_patcher.validator(self_prefix)
bot.labeler.vbml_patcher.validator(alias)

bot.labeler.vbml_ignore_case = True
for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.labeler.message_view.register_middleware(UserIgnore)

bot.session_manager = True
bot.ignore_error = True
bot.ask_each_event = True

if __name__ in "__main__":
    bot.run_forever()
