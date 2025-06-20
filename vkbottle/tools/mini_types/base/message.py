from __future__ import annotations

from abc import ABC, abstractmethod
from io import StringIO
from typing import TYPE_CHECKING, Any, Callable, Final, List, Literal, Optional, Union, overload

import pydantic
from vkbottle_types.objects import (
    AudioAudio,
    DocsDoc,
    MessagesAudioMessage,
    MessagesConversationMember,
    MessagesForward,
    MessagesMessage,
    PhotosPhoto,
    UsersUserFull,
    VideoVideoFull,
    WallWallComment,
    WallWallpostFull,
)

from vkbottle.modules import json, logger

if TYPE_CHECKING:
    from vkbottle_types.responses.messages import MessagesSendUserIdsResponseItem

    from vkbottle.api import ABCAPI, API

from vkbottle.dispatch.dispenser.base import StatePeer  # noqa: TC001
from vkbottle.tools.formatting import Format, Formatter

from .foreign_message import BaseForeignMessageMin  # noqa: TC001
from .mention import Mention, replace_mention_validator

MessageText = Union[str, Formatter, Format]

PEER_ID_OFFSET: Final[int] = 2_000_000_000


class BaseMessageMin(MessagesMessage, ABC):
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional[StatePeer] = None
    reply_message: Optional[BaseForeignMessageMin] = None
    fwd_messages: List[BaseForeignMessageMin] = pydantic.Field(default_factory=list)
    replace_mention: Optional[bool] = None
    _mention: Optional[Mention] = None
    _chat_members: Optional[List[MessagesConversationMember]] = None

    __replace_mention = pydantic.model_validator(mode="after")(replace_mention_validator)  # type: ignore

    model_config = pydantic.ConfigDict(frozen=False)

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return self.unprepared_ctx_api  # type: ignore

    @property
    def mention(self) -> Optional[Mention]:
        """Returns `Mention` object if message contains mention,
        eg if message is `@username text` returns `Mention(id=123, text="text")`,
        also mention is automatically removes from message text"""
        if not self.replace_mention:
            logger.warning(
                "labeler.message_view.replace_mention is set to False, the mention will not be processed"
            )
            return None
        return self._mention

    @property
    def chat_members(self) -> Optional[List["MessagesConversationMember"]]:
        return self._chat_members

    @property
    @abstractmethod
    def is_mentioned(self) -> bool:
        """Returns True if current bot is mentioned in message"""
        ...

    @overload
    async def get_user(self, raw_mode: Literal[False] = ..., **kwargs) -> "UsersUserFull": ...

    @overload
    async def get_user(self, raw_mode: Literal[True] = ..., **kwargs) -> dict: ...

    async def get_user(self, raw_mode: bool = False, **kwargs) -> Union["UsersUserFull", dict]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUserFull(**raw_user)

    async def get_chat_members(self, **kwargs: Any) -> List["MessagesConversationMember"]:
        if self._chat_members is None:
            self._chat_members = (
                await self.ctx_api.messages.get_conversation_members(
                    peer_id=self.peer_id,
                    **kwargs,
                )
            ).items
        return self._chat_members  # type: ignore

    async def user_is_admin(self, user_id: int, /) -> bool:
        members = await self.get_chat_members()
        if not members:
            return False
        return any(member.member_id == user_id and member.is_admin for member in members)

    @property
    def chat_id(self) -> int:
        return self.peer_id - PEER_ID_OFFSET

    @property
    def message_id(self) -> int:
        return self.id or self.conversation_message_id

    def get_attachment_strings(self) -> Optional[List[str]]:
        if self.attachments is None:
            return None

        attachments = []
        for attachment in self.attachments:
            attachment_type = attachment.type.value
            attachment_object = getattr(attachment, attachment_type)
            if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
                logger.debug("Got unsupported attachment type: {}", attachment_type)
                continue

            attachment_string = (
                f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
            )
            if hasattr(attachment_object, "access_key"):
                attachment_string += f"_{attachment_object.access_key}"

            attachments.append(attachment_string)

        return attachments

    def get_wall_attachment(self) -> Optional[List["WallWallpostFull"]]:
        if self.attachments is None:
            return None
        result = [attachment.wall for attachment in self.attachments if attachment.wall]
        return result or None

    def get_wall_reply_attachment(self) -> Optional[List["WallWallComment"]]:
        if self.attachments is None:
            return None
        result = [
            attachment.wall_reply for attachment in self.attachments if attachment.wall_reply
        ]
        return result or None

    def get_photo_attachments(self) -> Optional[List["PhotosPhoto"]]:
        if self.attachments is None:
            return None
        return [attachment.photo for attachment in self.attachments if attachment.photo]

    def get_video_attachments(self) -> Optional[List["VideoVideoFull"]]:
        if self.attachments is None:
            return None
        return [attachment.video for attachment in self.attachments if attachment.video]

    def get_doc_attachments(self) -> Optional[List["DocsDoc"]]:
        if self.attachments is None:
            return None
        return [attachment.doc for attachment in self.attachments if attachment.doc]

    def get_audio_attachments(self) -> Optional[List["AudioAudio"]]:
        if self.attachments is None:
            return None
        return [attachment.audio for attachment in self.attachments if attachment.audio]

    def get_audio_message_attachments(self) -> Optional[List["MessagesAudioMessage"]]:
        if self.attachments is None:
            return None
        return [
            attachment.audio_message for attachment in self.attachments if attachment.audio_message
        ]

    def get_message_id(self) -> Optional[int]:
        return self.id or self.conversation_message_id

    def get_payload_json(
        self,
        throw_error: bool = False,
        unpack_failure: Callable[[str], Union[dict, str]] = lambda payload: payload,
    ) -> Optional[Union[dict, str]]:
        if self.payload is None:
            return None

        try:
            return json.loads(self.payload)
        except (ValueError, TypeError) as e:
            if throw_error:
                raise e from None

        return unpack_failure(self.payload)

    async def answer(
        self,
        message: Optional[MessageText] = None,
        attachment: Optional[str] = None,
        random_id: Optional[int] = 0,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        forward: Optional[str] = None,
        sticker_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        template: Optional[str] = None,
        payload: Optional[str] = None,
        content_source: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        intent: Optional[str] = None,
        subscribe_id: Optional[int] = None,
        **kwargs: Any,
    ) -> "MessagesSendUserIdsResponseItem":
        if isinstance(message, (Formatter, Format)):
            kwargs["format_data"] = (
                message.raw_format_data
                if isinstance(message, Formatter)
                else message.as_raw_data()
            )

        data = self.ctx_api.messages.get_set_params(locals())
        deprecated_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        deprecated = [k for k in data if k in deprecated_params]
        if deprecated:
            logger.warning(
                "Params like peer_id or user_id is deprecated in Message.answer()."
                "Use API.messages.send() instead"
            )
            for k in deprecated:
                data.pop(k, None)

        if message is None:
            message = ""
        elif not isinstance(message, str):
            message = str(message)

        stream = StringIO(message)
        while True:
            if msg := stream.read(4096):
                data["message"] = msg

            response = (await self.ctx_api.messages.send(peer_ids=[self.peer_id], **data))[0]  # type: ignore
            if stream.tell() == len(message or ""):
                break

        return response

    async def reply(
        self,
        message: Optional[MessageText] = None,
        attachment: Optional[str] = None,
        **kwargs: Any,
    ) -> "MessagesSendUserIdsResponseItem":
        data = self.ctx_api.messages.get_set_params(locals())
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],  # type: ignore
            peer_id=self.peer_id,
            is_reply=True,
        ).model_dump_json()
        return await self.answer(**data)

    async def forward(
        self,
        message: Optional[MessageText] = None,
        attachment: Optional[str] = None,
        **kwargs: Any,
    ) -> "MessagesSendUserIdsResponseItem":
        data = self.ctx_api.messages.get_set_params(locals())
        data.pop("forward_message_ids", None)
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],
            peer_id=self.peer_id,  # type: ignore
        ).model_dump_json()
        return await self.answer(**data)


BaseMessageMin.model_rebuild()


__all__ = ("BaseMessageMin",)
