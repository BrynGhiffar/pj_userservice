from bson import ObjectId
from pymongo import ReturnDocument
from domain.classes.class_entity import Class
from bson.errors import InvalidId
from pymongo.errors import ServerSelectionTimeoutError

class ClassRepositoryError:

    def __init__(self):
        self.name = "GENERIC_CLASS_REPOSITORY_ERROR"
        self.message = "An unknown error occurred, please contact developer"

class ClassRepositoryErrorExtra(ClassRepositoryError):

    def __init__(self):
        super().__init__()
        self.extra_message = "Something must have gone wrong"
    
class TimeoutConnectionError(ClassRepositoryErrorExtra):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "CLASS_REPOSITORY_TIMEOUT_ERROR"
        self.message = "Connection with the database has timed out"
        self.extra_message = extra_message

class ClassRepository:

    def __init__(self, classes_repository_config):
        self.get_classes_collection = classes_repository_config

    def create_classes(self, classes: Class) -> Class \
                                            | TimeoutConnectionError \
                                            | None:
        classes_dict = classes.dict()
        del classes_dict["class_id"]

        try:
            res = self.get_classes_collection().insert_one(classes_dict)
        except ServerSelectionTimeoutError as e:
            return TimeoutConnectionError(extra_message=e._message)
        classes.class_id = str(res.inserted_id)
        return classes

    def find_classes_by_id(self, class_id: str) -> Class \
                                            | TimeoutConnectionError \
                                            | None:
        try:
            _id = ObjectId(class_id)
            try:
                res = self.get_classes_collection().find_one({"_id": _id})
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)

            # if no classes with the id was found, return None
            if not res:
                return None
            
            res["class_id"] = str(res["_id"])

            classes = Class.parse_obj(res)
            return classes
        except InvalidId:
            return None
    
    # Need bug fixing
    # def find_all_classes(self) -> list[Class] \
    #                             | TimeoutConnectionError \
    #                             :
    #     try:
    #         res = self.get_classes_collection().find()
    #     except ServerSelectionTimeoutError as e:
    #         return TimeoutConnectionError(extra_message=e._message)
    #     ret = []
    #     try:
    #         for classes in res:
    #             classes["class_id"] = str(classes["_id"])
    #             ret.append(Class.parse_obj(classes))
    #         return ret[::-1]
    #     except ServerSelectionTimeoutError as e:
    #         return TimeoutConnectionError(extra_message=e._message)
                            
    def update_class(self, classes: Class) -> Class \
                                        | TimeoutConnectionError \
                                        | None:
        try:
            _id = ObjectId(classes.class_id)
            try:
                res = self.get_classes_collection().find_one_and_replace({"_id": _id}, classes.dict(), return_document=ReturnDocument.AFTER)
            except ServerSelectionTimeoutError as e:
                return TimeoutConnectionError(extra_message=e._message)
            if not res:
                return None
            res["class_id"] = str(res["_id"])
            classes = Class.parse_obj(res)
            return classes
        except InvalidId:
            return None