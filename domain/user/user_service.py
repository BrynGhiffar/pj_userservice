import adapter.repository.user_repository as user_repository
from domain.user.user_entity import User

class Error:
    pass

class EmailAlreadyExistsError(Error):
    pass

class ProviderIdAlreadyExistsError(Error):
    pass

class UserNotFoundError(Error):
    pass

def find_user_by_id(user_id: str) -> User | None:
    res = user_repository.find_user_by_id(user_id)
    if not res:
        return None
    return res

def find_user_by_provider_id(provider: str, provider_id: str) -> User | None:
    res = user_repository.find_user_by_provider_id(provider, provider_id)
    if not res:
        return None
    return res

def create_user(user: User) -> User | None:

    if user.provider and user.provider_id:
        user_by_provider_id = user_repository.find_user_by_provider_id(user.provider, user.provider_id)
        if user_by_provider_id:
            return None
    

    if user.email:
        user_by_email = user_repository.find_user_by_email(user.email)
        if user_by_email:
            return None
    else:
        return None
    
    user = user_repository.create_user(user)
    if not user:
        return None
    return user

def update_user(user: User) -> User | Error:
    user_by_email = user_repository.find_user_by_email(user.email)
    if user_by_email and (user.user_id != user_by_email.user_id):
        return EmailAlreadyExistsError()
    if user.provider and user.provider_id:
        user_by_provider = user_repository.find_user_by_provider_id(user.provider, user.provider_id)
        if user_by_provider and (user.user_id != user_by_provider.user_id):
            return ProviderIdAlreadyExistsError()

    user = user_repository.update_user(user)
    if not user:
        return UserNotFoundError()
    return user

def update_user_description(user_id: str, description: str) -> User | None:
    user = user_repository.find_user_by_id(user_id)
    if not user:
        return None
    user.description = description
    new_user = user_repository.update_user(user)
    if not user:
        return None
    return new_user