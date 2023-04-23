import abc

from domain.user.user import User


class UserPersistenceInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def get_all(self) -> list[User]:
        pass

    # DONE homework: delete & edit

    @abc.abstractmethod
    def edit(self, user_id: str, username: str):
        pass

    @abc.abstractmethod
    def delete(self, user_id: str):
        pass
