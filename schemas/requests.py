from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field, TypeAdapter


class ConnectRequest(BaseModel):
    request_type: Literal['connect'] = 'connect'
    uid: str
    x: int
    y: int


class PositionUpdateRequest(BaseModel):
    request_type: Literal['position_update'] = 'position_update'
    x: int
    y: int


ValidatorModel = Annotated[
    Union[
        ConnectRequest,
        PositionUpdateRequest,
    ], Field(discriminator="request_type")]
adaptor = TypeAdapter(ValidatorModel)
