from asyncio import StreamReader, StreamWriter
from uuid import UUID
from pydantic import BaseModel


class Connection:
    def __init__(
            self,
            reader: StreamReader,
            writer: StreamWriter
    ):
        self.reader = reader
        self.writer = writer


class User:
    def __init__(
            self,
            uid: str,
            x: int,
            y: int,
            connection: Connection
    ):
        self.uid = uid
        self.x = x
        self.y = y
        self.connection = connection

    async def send_event(self, event: BaseModel):
        json_event = event.model_dump_json()
        print(json_event)
        self.connection.writer.write((json_event + "\n").encode())
        await self.connection.writer.drain()

    def to_dict(self):
        return {"uid": self.uid, "x": self.x, "y": self.y}
