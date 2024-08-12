from typing import Literal, Annotated, Union

from pydantic import BaseModel, Field, TypeAdapter


class UserResponse(BaseModel):
    uid: str
    x: int
    y: int


###
class CurrentUsers(BaseModel):
    request_type: Literal['user_list'] = 'user_list'
    users: list[UserResponse]


class UserConnected(BaseModel):
    request_type: Literal['new_user'] = 'new_user'
    uid: str
    x: int
    y: int


class UserDisconnected(BaseModel):
    request_type: Literal['delete_user'] = 'delete_user'
    uid: str


class UserPositionUpdated(BaseModel):
    request_type: Literal['user_position'] = 'user_position'
    uid: str
    x: int
    y: int


ValidatorModel = Annotated[
    Union[
        CurrentUsers,
        UserConnected,
        UserDisconnected,
        UserPositionUpdated,
    ], Field(discriminator="request_type")]
adaptor = TypeAdapter(ValidatorModel)
