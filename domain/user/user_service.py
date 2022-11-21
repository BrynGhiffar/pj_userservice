from adapter.repository.user_repository import UserRepository
from domain.user.user_entity import User

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

class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def find_user_by_id(self, user_id: str) -> User | UserWithUserIdNotFoundError:
        res = self.user_repository.find_user_by_id(user_id)
        if not res:
            return UserWithUserIdNotFoundError(user_id)
        return res

    def find_user_by_provider_id(self, provider: str, provider_id: str) -> User | UserWithProviderIdNotFoundError:


        res = self.user_repository.find_user_by_provider_id(provider, provider_id)
        if not res:
            return UserWithProviderIdNotFoundError(provider, provider_id)
        return res

    def create_user(self, user: User) -> User \
                                        | UserWithProviderIdAlreadyExistsError \
                                        | UserWithEmailAlreadyExistsError \
                                        | UserCreationError:


        # PROVIDER ID VALIDATION
        if user.provider and user.provider_id:
            user_by_provider_id = self.user_repository.find_user_by_provider_id(user.provider, user.provider_id)
            if user_by_provider_id:
                return UserWithProviderIdAlreadyExistsError(user.provider, user.provider_id)
        

        # EMAIL VALIDATION
        if user.email:
            user_by_email = self.user_repository.find_user_by_email(user.email)
            if user_by_email:
                return UserWithEmailAlreadyExistsError(user.email)
        else:
            return UserMissingEmailError()
        

        # CREATING THE USER
        user = self.user_repository.create_user(user)
        if not user:
            return UserCreationError()
        return user

    def update_user(self, user: User) -> User \
                                        | UserWithEmailAlreadyExistsError \
                                        | UserWithProviderIdAlreadyExistsError:

        # USER EXISTS VALIDATION
        # to check if the user with the id exists
        find_user = self.user_repository.find_user_by_id(user.user_id)
        if not find_user:
            return UserWithUserIdNotFoundError(user.user_id)

        # EMAIL UPDATE VALIDATION
        # for if the user wants to change their email. checks if the email to be changed to
        # already exists
        user_by_email = self.user_repository.find_user_by_email(user.email)
        if user_by_email and (user.user_id != user_by_email.user_id):
            return UserWithEmailAlreadyExistsError(user.email, extra_message="email cannot be changed")
        
        # PROVIDER ID VALIDATION
        # for if the user wants to change their provider id.
        # checks if the provider id to be changed to already exists
        if user.provider and user.provider_id:
            user_by_provider = self.user_repository.find_user_by_provider_id(user.provider, user.provider_id)
            if user_by_provider and (user.user_id != user_by_provider.user_id):
                return UserWithProviderIdAlreadyExistsError(user.provider, user.provider_id, extra_message="provider id cannot be changed")

        # UPDATING
        updated_user = self.user_repository.update_user(user)
        if not updated_user:
            return UserWithUserIdNotFoundError(user.user_id)
        return updated_user

    def update_user_description(self, user_id: str, description: str) -> User \
                                                                        | UserWithUserIdNotFoundError \
                                                                        | UserUpdateError:
        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            return UserWithUserIdNotFoundError(user_id)
        user.description = description
        new_user = self.user_repository.update_user(user)
        if not user:
            return UserUpdateError()
        return new_user