from bson import ObjectId
from pymongo import ReturnDocument
from domain.user.user_entity import User
from bson.errors import InvalidId
from pymongo.errors import ServerSelectionTimeoutError

class UserRepositoryError:

    def __init__(self):
        self.name = "GENERIC_USER_REPOSITORY_ERROR"
        self.message = "An unknown error occurred, please contact developer"

class UserRepositoryErrorExtra(UserRepositoryError):

    def __init__(self):
        super().__init__()
        self.extra_message = "Something must have gone wrong"
    
class TimeoutConnectionError(UserRepositoryErrorExtra):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "USER_REPOSITORY_TIMEOUT_ERROR"
        self.message = "Connection with the database has timed out"
        self.extra_message = extra_message

class UserRepository:

    def __init__(self, user_repository_config):
        self.get_user_collection = user_repository_config

    def create_user(self, user: User) -> User \
                                            | TimeoutConnectionError \
                                            | None:
        user_dict = user.dict()
        del user_dict["user_id"]
        try:
            res = self.get_user_collection().insert_one(user_dict)
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        user.user_id = str(res.inserted_id)
        return user

    def find_user_by_id(self, user_id: str) -> User \
                                            | TimeoutConnectionError \
                                            | None:
        try:
            _id = ObjectId(user_id)
            try:
                res = self.get_user_collection().find_one({"_id": _id})
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)

            # if no user with the id was found, return None
            if not res:
                return None
            
            res["user_id"] = str(res["_id"])

            user = User.parse_obj(res)
            return user
        except InvalidId:
            return None

    def find_user_by_provider_id(self, provider: str, provider_id: str) -> User \
                                                                            | TimeoutConnectionError \
                                                                            | None:
        try:
            res = self.get_user_collection().find_one({"provider": provider, "provider_id": provider_id})
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        if not res:
            return None
        res["user_id"] = str(res["_id"])
        user = User.parse_obj(res)
        return user

    def find_user_by_email(self, email: str) -> User \
                                                | TimeoutConnectionError \
                                                | None:
        try:
            res = self.get_user_collection().find_one({"email": email})
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        if not res:
            return None
        res["user_id"] = str(res["_id"])
        user = User.parse_obj(res)
        return user

    def update_user(self, user: User) -> User \
                                        | TimeoutConnectionError \
                                        | None:
        try:
            _id = ObjectId(user.user_id)
            try:
                res = self.get_user_collection().find_one_and_replace({"_id": _id}, user.dict(), return_document=ReturnDocument.AFTER)
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)
            if not res:
                return None
            res["user_id"] = str(res["_id"])
            user = User.parse_obj(res)
            return user
        except InvalidId:
            return None