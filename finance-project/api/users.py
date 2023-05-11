import json
from fastapi import APIRouter, Depends

from domain.asset.factory import AssetFactory
from domain.user.repo import UserRepo
from api.models import UserAdd, UserInfo, AssetInfoUser, AssetAdd
from domain.user.factory import UserFactory
from persistence.user_file import UserPersistenceFile
from persistence.user_sqlite import UserPersistenceSqlite

users_router = APIRouter(prefix="/users")


class InvalidPersistenceType(Exception):
    pass


def check_persistence_type(file_path):
    with open(file_path, 'r') as config_info:
        persistence_type = config_info.read()
        data = json.loads(persistence_type)
        if "sqlite" in str(data["persistence"]):
            return UserPersistenceSqlite()
        elif "json" in str(data["persistence"]):
            return UserPersistenceFile("main_users.json")
        else:
            raise InvalidPersistenceType("Unrecognized persistence config type. Please check config.json file.")


def get_user_repo() -> UserRepo:
    user_persistence = check_persistence_type("config.json")
    # user_persistence = UserPersistenceFile("main_users.json")
    # user_persistence = UserPersistenceSqlite()
    return UserRepo(user_persistence)


# Homework 1 for Project
# implement get, create and delete user in domain too (user repo & user factory)
# also create api models
# create tests for repo & factory
# username should be at least 6 chars and max 20 chars, it can only contain letter, numbers & -
# save the user list in a file


@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all_users()


# TODO homework, replace username with an id
# when we create a user we should create an uuid for it
# when we return all the users, each user should have the id field
# when we query a single user or delete a user we should pass the id

# create POST /<user_id>/stocks
# the user can add a stock to its portfolio, by giving the ticker and the number of units it has
# save the country, full name of the company
# when we get a specific user we get the price of every stock the user has and the money it has on it


# DONE get /users/{user_id}
@users_router.get("/{user_id}", response_model=UserInfo)
def get_user_by_id(user_id: str, repo=Depends(get_user_repo)):
    return repo.get_by_id(user_id)


# @users_router.get("/{username}", response_model=UserInfo)
# def get_user(username: str, repo=Depends(get_user_repo)):
#     return repo.get_by_username(username)


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    user = UserFactory().make_new(new_user.username)
    repo.add(user)
    return user


# DONE delete a user, DELETE /users/{user_id}
@users_router.delete("/{user_id}")
def delete_a_user(user_id: str, repo=Depends(get_user_repo)):
    repo.delete(user_id)


# DONE probably add edit user by id
@users_router.put("/{user_id}", response_model=UserInfo)
def edit_user(user_id: str, username: str, repo=Depends(get_user_repo)):
    repo.edit(user_id, username)
    return repo.get_by_id(user_id)


# TODO fix api, return asset info


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(user_id: str, asset: AssetAdd, repo=Depends(get_user_repo)):
    new_asset = AssetFactory().make_new(
        asset.ticker
    )  # TODO homework, if asset exception throw 400/404
    user = repo.get_by_id(
        user_id
    )  # TODO, check we have a user otherwise throw exception code 404
    # user.add_stock(new_asset)
    repo.add_to_user(user, new_asset)
    return new_asset
