import asyncio

from entities.entities import User, Connection
from manager.user_manager import UserManager
from schemas.requests import ConnectRequest, PositionUpdateRequest
from schemas.responses import CurrentUsers, UserConnected, UserDisconnected, UserPositionUpdated
from utils import read_message, broadcast, get_request_model
from data import settings

user_manager = UserManager()


async def connect(reader, writer) -> User:
    message = await read_message(reader)
    request = ConnectRequest.model_validate_json(message)

    user = User(
        request.uid,
        request.x,
        request.y,
        Connection(reader, writer)
    )

    user_manager.add_user(user)

    users = user_manager.get_users()

    event_personal = CurrentUsers(
        users=[user.to_dict() for user in users if user.uid != request.uid]
    )

    event_global = UserConnected(
        uid=request.uid,
        x=request.x,
        y=request.y,
    )

    await user.send_event(event_personal)
    await broadcast(users, event_global, request.uid)

    return user


async def disconnect(user: User):
    user_manager.remove_user(user)
    users = user_manager.get_users()

    event = UserDisconnected(
        uid=user.uid
    )

    await broadcast(users, event, user.uid)


async def proceed_event(user: User, request: str):
    request = get_request_model(request)

    try:
        if isinstance(request, PositionUpdateRequest):
            users = user_manager.get_users()
            event = UserPositionUpdated(
                uid=user.uid,
                x=request.x,
                y=request.y,
            )
            await broadcast(
                users,
                event,
                user.uid
            )
            print(f"| User with uid: {user.uid} has position: ({request.x} {request.y})|")
    except Exception as e:
        print(e)


async def event_handler(reader, writer):
    print("Connection Established")

    try:
        user = await connect(reader, writer)
    except Exception as e:
        return

    while True:
        try:
            message = await read_message(reader)
        except Exception as e:
            await disconnect(user)
            return
        if message == "":
            await disconnect(user)
            break
        await proceed_event(user, message)


async def main():
    server = await asyncio.start_server(
        event_handler,
        settings['host'],
        settings['port']
    )

    async with server:
        await server.serve_forever()


asyncio.run(main())
