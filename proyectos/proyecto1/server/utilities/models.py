from pydantic import BaseModel  # type: ignore


class Contract(BaseModel):
    customer_id: int
    date: str
    value: int
    aditional: int
    payment: int
    renewal: int
    article: str


class User(BaseModel):
    name: str
    surname: str
    document: str
    email: str
