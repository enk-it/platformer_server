from asyncio import StreamReader

from pydantic import BaseModel

from entities.entities import User
from schemas.requests import adaptor


async def read_message(reader: StreamReader) -> str:
    data = await reader.readline()
    message = data.decode().strip()
    return message


def get_request_model(data: str):
    return adaptor.validate_json(data)


async def broadcast(users: [User], event: BaseModel, sender_user_id: str):
    for user in users:
        if user.uid != sender_user_id:
            await user.send_event(event)
