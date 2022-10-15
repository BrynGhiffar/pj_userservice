from importlib.abc import ResourceLoader
from bson import ObjectId
from pymongo import ReturnDocument
from adapter.repository.config import get_database
from domain.user.user_entity import User
from bson.errors import InvalidId

user_collection = lambda: get_database()["user"]

def create_user(user: User) -> User | None:
    res = user_collection().insert_one(user.dict())
    user.user_id = str(res.inserted_id)
    return user

def find_user_by_id(user_id: str) -> User | None:
    try:
        _id = ObjectId(user_id)
        res = user_collection().find_one({"_id": _id})

        # if no user with the id was found, return None
        if not res:
            return None
        
        res["user_id"] = str(res["_id"])

        user = User.parse_obj(res)
        return user
    except InvalidId:
        return None

def find_user_by_provider_id(provider: str, provider_id: str) -> User | None:
    res = user_collection().find_one({"provider": provider, "provider_id": provider_id})
    if not res:
        return None
    res["user_id"] = str(res["_id"])
    user = User.parse_obj(res)
    return user

def find_user_by_email(email: str) -> User | None:
    res = user_collection().find_one({"email": email})
    if not res:
        return None
    res["user_id"] = str(res["_id"])
    user = User.parse_obj(res)
    return user

def update_user(user: User) -> User | None:
    try:
        _id = ObjectId(user.user_id)
        res = user_collection().find_one_and_replace({"_id": _id}, user.dict(), return_document=ReturnDocument.AFTER)
        if not res:
            return None
        res["user_id"] = str(res["_id"])
        user = User.parse_obj(res)
        return user
    except InvalidId:
        return None