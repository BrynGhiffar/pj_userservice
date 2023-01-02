from adapter.repository.class_repository import ClassRepository
from domain.classes.class_entity import Class
from domain.notification.notification_service import NotificationService
from adapter.repository.class_repository import TimeoutConnectionError

class ClassServiceError:
    def __init__(self):
        self.name = "ERROR"
        self.message = "An unspecific error occurred, please contact developer"

class ClassServiceExtraError(ClassServiceError):
    def __init__(self):
        self.extra_message = ""

class ClassWithClassIdNotFoundError(ClassServiceError):

    def __init__(self, class_id: str):
        self.name = "CLASS_ID_NOT_EXISTS"
        self.class_id = class_id
        self.message = f"class with id '{self.class_id}' was not found"

class ClassCreationError(ClassServiceError):

    def __init__(self):
        self.name = "CLASS_CREATION_ERROR"
        self.message = "Class could not be created for some reason, please contact developer"

class ClassUpdateError(ClassServiceError):

    def __init__(self):
        self.name = "CLASS_UPDATE_ERROR"
        self.message = "class could not be updated for some reason, please contact developer"

class DatabaseConnectionError(ClassServiceExtraError):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "DATABASE_CONNECTION_ERROR"
        self.message = "There was a problem connecting to the database"
        self.extra_message = extra_message

class ClassService:

    def __init__(self, class_repository: ClassRepository, notification_service: NotificationService):
        self.class_repository = class_repository
        self.notification_service = notification_service

    def find_class_by_id(self, class_id: str) -> Class \
                                                | DatabaseConnectionError \
                                                | ClassWithClassIdNotFoundError \
                                                :
        res = self.class_repository.find_classes_by_id(class_id)
        if isinstance(res, TimeoutConnectionError):
            return DatabaseConnectionError(res.extra_message)
        if not res:
            return ClassWithClassIdNotFoundError(class_id)
        return res

    def find_class_by_id(self, lecturer_id: str) -> Class \
                                                | DatabaseConnectionError \
                                                | ClassWithClassIdNotFoundError \
                                                :
        res = self.class_repository.find_classes_by_lecturer_id(lecturer_id)
        if isinstance(res, TimeoutConnectionError):
            return DatabaseConnectionError(res.extra_message)
        if not res:
            return ClassWithClassIdNotFoundError(lecturer_id)
        return res

    def create_class(self, classes: Class) -> Class \
                                        | ClassCreationError \
                                        | DatabaseConnectionError \
                                        :
    
        # CREATING THE CLASS
        created_classes = self.class_repository.create_classes(classes)
        if isinstance(created_classes, TimeoutConnectionError):
            return DatabaseConnectionError(created_classes.extra_message)
        if not created_classes:
            return ClassCreationError()
        
        # SEND CLASS CREATED NOTIFICATION
        class_id = created_classes.class_id if created_classes.class_id else "no classes id, this is a problem"
        self.notification_service.send_classes_created_notification(class_id, classes.name)

        return classes

    def update_classes(self, classes: Class) -> Class \
                                        | ClassWithClassIdNotFoundError \
                                        | DatabaseConnectionError \
                                        :

        # CLASS EXISTS VALIDATION
        if classes.class_id is None:
            return ClassWithClassIdNotFoundError("None")
        # to check if the classes with the id exists
        find_classes = self.class_repository.find_classes_by_id(classes.class_id)
        if isinstance(find_classes, TimeoutConnectionError):
            return DatabaseConnectionError(find_classes.extra_message)
        if not find_classes:
            return ClassWithClassIdNotFoundError(classes.class_id)

        # UPDATING
        updated_classes = self.class_repository.update_class(classes)
        if isinstance(updated_classes, TimeoutConnectionError):
            return DatabaseConnectionError(updated_classes.extra_message)
        if not updated_classes:
            return ClassWithClassIdNotFoundError(classes.class_id)
        return updated_classes
    
    # Need bug fixing
    def find_all_classes(self) -> list[Class] | DatabaseConnectionError:
        all_classes = self.class_repository.find_all_classes()
        if isinstance(all_classes, TimeoutConnectionError):
            return DatabaseConnectionError(all_classes.extra_message)
        return all_classes