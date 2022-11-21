from bson import ObjectId
from pymongo import ReturnDocument
from adapter.repository.config import get_database
from domain.user.user_entity import User
from bson.errors import InvalidId

user_collection = lambda: get_database()["user"]

class UserRepository:

    def __init__(self, user_repository_config):
        self.get_user_collection = user_repository_config

    def create_user(self, user: User) -> User | None:
        user_dict = user.dict()
        del user_dict["user_id"]
        res = self.get_user_collection().insert_one(user_dict)
        user.user_id = str(res.inserted_id)
        return user

    def find_user_by_id(self, user_id: str) -> User | None:
        try:
            _id = ObjectId(user_id)
            res = self.get_user_collection().find_one({"_id": _id})

            # if no user with the id was found, return None
            if not res:
                return None
            
            res["user_id"] = str(res["_id"])

            user = User.parse_obj(res)
            return user
        except InvalidId:
            return None

    def find_user_by_provider_id(self, provider: str, provider_id: str) -> User | None:
        res = self.get_user_collection().find_one({"provider": provider, "provider_id": provider_id})
        if not res:
            return None
        res["user_id"] = str(res["_id"])
        user = User.parse_obj(res)
        return user

    def find_user_by_email(self, email: str) -> User | None:
        res = self.get_user_collection().find_one({"email": email})
        if not res:
            return None
        res["user_id"] = str(res["_id"])
        user = User.parse_obj(res)
        return user

    def update_user(self, user: User) -> User | None:
        try:
            _id = ObjectId(user.user_id)
            res = self.get_user_collection().find_one_and_replace({"_id": _id}, user.dict(), return_document=ReturnDocument.AFTER)
            if not res:
                return None
            res["user_id"] = str(res["_id"])
            user = User.parse_obj(res)
            return user
        except InvalidId:
            return None