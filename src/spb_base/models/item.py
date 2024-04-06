from beanie import Document


class Item(Document):
    name: str
    code: str
    description: str
