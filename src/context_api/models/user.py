from pydantic import BaseModel


class User(BaseModel):
    id: int


class Guest(User):
    pass


class Member(User):
    username: str
    email: str
    disabled: bool


class Subscriber(Member):
    subscription_type: str
