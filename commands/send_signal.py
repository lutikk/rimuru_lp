from vkbottle.user import Message, UserLabeler

from models import User
from utils import send_request

bl = UserLabeler()

bl.vbml_ignore_case = True


@bl.message(text='<pref:self_prefix> <text>')
async def greeting(message: Message, text: str):
    user_db = User.load()
    if not user_db.id == message.from_id:
        return
    __model = {
        "user_id": message.from_id,
        "method": "lpSendMySignal",
        "secret": user_db.secret_code,
        "message": {
            "conversation_message_id": message.conversation_message_id,
            "from_id": message.from_id,
            "date": message.date,
            "text": '.с' + ' ' + text,
            "peer_id": message.peer_id
        },
        "object": {
            "chat": None,
            "from_id": message.from_id,
            "value": text,
            "conversation_message_id": message.conversation_message_id
        },
    }
    await send_request(__model, message)
