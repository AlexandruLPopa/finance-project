import uuid
from fastapi import FastAPI
from domain.user.user import User


class InvalidUsername(Exception):
    pass


class UserFactory:
    def make_new(self, username: str) -> User:
        # DONE rest of validations
        uname = username.split("-")
        uname_str = ""
        for u in uname:
            uname_str += u
        if not uname_str.isalnum():
            raise InvalidUsername(
                "Username should be alphanumeric and can only contain the symbol '-'."
            )
        if len(username) > 20:
            raise InvalidUsername("Username should have less than 20 characters.")
        if len(username) < 6:
            raise InvalidUsername("Username should have at least 6 characters.")
        user_uuid = uuid.uuid4()
        return User(user_uuid, username)

    def make_from_persistence(self, info: tuple) -> User:
        return User(
            uuid=uuid.UUID(info[0]),
            username=info[1],
        )
