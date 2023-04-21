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
    def edit_by_id(self, user_id: User.id, username: str):
        pass

    @abc.abstractmethod
    def delete_by_id(self, user_id: User.id):
        pass
