from adapter.repository.user_repository import UserRepository
from domain.user.user_entity import User
from domain.notification.notification_service import NotificationService
from adapter.repository.user_repository import TimeoutConnectionError

class UserServiceError:
    def __init__(self):
        self.name = "ERROR"
        self.message = "An unspecific error occurred, please contact developer"

class UserServiceExtraError(UserServiceError):
    def __init__(self):
        self.extra_message = ""

class UserWithEmailAlreadyExistsError(UserServiceExtraError):

    def __init__(self, email: str, extra_message: str = ""):
        self.name = "USER_EMAIL_ID_EXISTS"
        self.email = email
        self.message = f"user with email '{self.email}' already exists"
        self.extra_message = extra_message

class UserWithProviderIdAlreadyExistsError(UserServiceExtraError):

    def __init__(self, provider: str, provider_id: str, extra_message: str = ""):
        self.name = "USER_PROVIDER_ID_EXISTS"
        self.provider = provider
        self.provider_id = provider_id
        self.message = f"user with id '{self.provider}:{self.provider_id}' already exists"
        self.extra_message = extra_message

class UserWithUserIdNotFoundError(UserServiceError):

    def __init__(self, user_id: str):
        self.name = "USER_ID_NOT_EXISTS"
        self.user_id = user_id
        self.message = f"user with id '{self.user_id}' was not found"

class UserWithProviderIdNotFoundError(UserServiceError):

    def __init__(self, provider: str, provider_id: str):
        self.name = "USER_PROVIDER_ID_NOT_EXISTS"
        self.provider = provider
        self.provider_id = provider_id
        self.message = f"user with id '{self.provider}:{self.provider_id}' is not found"

class UserMissingEmailError(UserServiceError):

    def __init__(self):
        self.name = "USER_MISSING_EMAIL"
        self.message = "user email is missing, email field cannot be empty"

class UserCreationError(UserServiceError):

    def __init__(self):
        self.name = "USER_CREATION_ERROR"
        self.message = "User could not be created for some reason, please contact developer"

class UserUpdateError(UserServiceError):

    def __init__(self):
        self.name = "USER_UPDATE_ERROR"
        self.message = "user could not be updated for some reason, please contact developer"

class DatabaseConnectionError(UserServiceExtraError):

    def __init__(self, extra_message: str):
        super().__init__()
        self.name = "DATABASE_CONNECTION_ERROR"
        self.message = "There was a problem connecting to the database"
        self.extra_message = extra_message

class UserService:

    def __init__(self, user_repository: UserRepository, notification_service: NotificationService):
        self.user_repository = user_repository
        self.notification_service = notification_service

    def find_user_by_id(self, user_id: str) -> User \
                                                | DatabaseConnectionError \
                                                | UserWithUserIdNotFoundError \
                                                :
        res = self.user_repository.find_user_by_id(user_id)
        if isinstance(res, TimeoutConnectionError):
            return DatabaseConnectionError(res.extra_message)
        if not res:
            return UserWithUserIdNotFoundError(user_id)
        return res

    def find_user_by_provider_id(self, provider: str, provider_id: str) -> User \
                                                                            | DatabaseConnectionError \
                                                                            | UserWithProviderIdNotFoundError \
                                                                            :


        res = self.user_repository.find_user_by_provider_id(provider, provider_id)
        if isinstance(res, TimeoutConnectionError):
            return DatabaseConnectionError(extra_message=res.message)
        if not res:
            return UserWithProviderIdNotFoundError(provider, provider_id)
        return res

    def create_user(self, user: User) -> User \
                                        | UserWithProviderIdAlreadyExistsError \
                                        | UserWithEmailAlreadyExistsError \
                                        | UserMissingEmailError \
                                        | UserCreationError \
                                        | DatabaseConnectionError \
                                        :


        # PROVIDER ID VALIDATION
        if user.provider and user.provider_id:
            user_by_provider_id = self.user_repository.find_user_by_provider_id(user.provider, user.provider_id)
            if isinstance(user_by_provider_id, TimeoutConnectionError):
                return DatabaseConnectionError(user_by_provider_id.extra_message)
            if user_by_provider_id:
                return UserWithProviderIdAlreadyExistsError(user.provider, user.provider_id)
        

        # EMAIL VALIDATION
        if user.email:
            user_by_email = self.user_repository.find_user_by_email(user.email)
            if isinstance(user_by_email, TimeoutConnectionError):
                return DatabaseConnectionError(user_by_email.extra_message)
            if user_by_email:
                return UserWithEmailAlreadyExistsError(user.email)
        else:
            return UserMissingEmailError()
        

        # CREATING THE USER
        created_user = self.user_repository.create_user(user)
        if isinstance(created_user, TimeoutConnectionError):
            return DatabaseConnectionError(created_user.extra_message)
        if not created_user:
            return UserCreationError()
        
        # SEND USER CREATED NOTIFICATION
        user_id = created_user.user_id if created_user.user_id else "no user id, this is a problem"
        email = created_user.email if not (created_user.email is None) else "no email, this is a problem"
        self.notification_service.send_user_created_notification(user_id, email, user.name)

        return user

    def update_user(self, user: User) -> User \
                                        | UserWithUserIdNotFoundError \
                                        | DatabaseConnectionError \
                                        | UserWithEmailAlreadyExistsError \
                                        | UserWithProviderIdAlreadyExistsError \
                                        :

        # USER EXISTS VALIDATION
        if user.user_id is None:
            return UserWithUserIdNotFoundError("None")
        # to check if the user with the id exists
        find_user = self.user_repository.find_user_by_id(user.user_id)
        if isinstance(find_user, TimeoutConnectionError):
            return DatabaseConnectionError(find_user.extra_message)
        if not find_user:
            return UserWithUserIdNotFoundError(user.user_id)

        # EMAIL UPDATE VALIDATION
        # for if the user wants to change their email. checks if the email to be changed to
        # already exists
        user_by_email = self.user_repository.find_user_by_email(user.email)
        if isinstance(user_by_email, TimeoutConnectionError):
            return DatabaseConnectionError(user_by_email.extra_message)
        if user_by_email and (user.user_id != user_by_email.user_id):
            return UserWithEmailAlreadyExistsError(user.email, extra_message="email cannot be changed")
        
        # PROVIDER ID VALIDATION
        # for if the user wants to change their provider id.
        # checks if the provider id to be changed to already exists
        if user.provider and user.provider_id:
            user_by_provider = self.user_repository.find_user_by_provider_id(user.provider, user.provider_id)
            if isinstance(user_by_provider, TimeoutConnectionError):
                return DatabaseConnectionError(user_by_provider.extra_message)
            if user_by_provider and (user.user_id != user_by_provider.user_id):
                return UserWithProviderIdAlreadyExistsError(user.provider, user.provider_id, extra_message="provider id cannot be changed")

        # UPDATING
        updated_user = self.user_repository.update_user(user)
        if isinstance(updated_user, TimeoutConnectionError):
            return DatabaseConnectionError(updated_user.extra_message)
        if not updated_user:
            return UserWithUserIdNotFoundError(user.user_id)
        return updated_user

    def update_user_description(self, user_id: str, description: str) -> User \
                                                                        | UserWithUserIdNotFoundError \
                                                                        | UserUpdateError \
                                                                        | DatabaseConnectionError \
                                                                        :
        user = self.user_repository.find_user_by_id(user_id)
        if isinstance(user, TimeoutConnectionError):
            return DatabaseConnectionError(user.extra_message)
        if not user:
            return UserWithUserIdNotFoundError(user_id)
        user.description = description
        new_user = self.user_repository.update_user(user)
        if isinstance(new_user, TimeoutConnectionError):
            return DatabaseConnectionError(new_user.extra_message)
        if not new_user:
            return UserUpdateError()
        return new_user
    
    def find_all_user(self) -> list[User] | DatabaseConnectionError:
        all_user = self.user_repository.find_all_user()
        if isinstance(all_user, TimeoutConnectionError):
            return DatabaseConnectionError(all_user.extra_message)
        return all_user

    def find_user_by_name(self, name:str) -> list[User] | DatabaseConnectionError:
        all_user = self.user_repository.find_user_by_name(name)
        if isinstance(all_user, TimeoutConnectionError):
            return DatabaseConnectionError(all_user.extra_message)
        return all_user
