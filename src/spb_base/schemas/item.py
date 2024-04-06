from beanie import PydanticObjectId
from pydantic import BaseModel


class CreateItem(BaseModel):
    name: str
    code: str
    description: str


class ItemResponse(CreateItem):
    id: PydanticObjectId
    name: str
    code: str
    description: str
