from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from domain.user.user_entity import User
from domain.user.user_service import UserServiceError, \
                                    UserService, \
                                    UserServiceExtraError

class CreateUserResponse(BaseModel):
    message: str
    user: User | None

class FindUserByIdResponse(BaseModel):
    message: str
    user: User | None

class FindUserByProviderResponse(BaseModel):
    message: str
    user: User | None

class UpdateUserResponse(BaseModel):
    message: str
    user: User | None


class UpdateUserDescriptionBody(BaseModel):
    user_id: str
    description: str

class UpdateUserDescriptionResponse(BaseModel):
    message: str
    user: User | None


class UserHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def find_user_by_id(self, user_id: str):
        res = self.user_service.find_user_by_id(user_id)
        if isinstance(res, UserServiceError):
            find_user_by_id_response = jsonable_encoder(FindUserByIdResponse(
                message=f"{res.name}: {res.message}",
                user=None
            ))
            return JSONResponse(content=find_user_by_id_response, status_code=404, media_type="application/json")
        else:
            find_user_by_id_response = jsonable_encoder(FindUserByIdResponse(
                message="user found",
                user=res
            ))
            return JSONResponse(content=find_user_by_id_response, status_code=200, media_type="application/json")

    def find_user_by_provider(self, provider: str, provider_id: str):
        res = self.user_service.find_user_by_provider_id(provider, provider_id)
        if isinstance(res, UserServiceExtraError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, UserServiceError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            find_user_by_provider = jsonable_encoder(FindUserByProviderResponse(
                message="user found",
                user=res
            ))
            return JSONResponse(content=find_user_by_provider, status_code=200, media_type="application/json")
        
    def create_user(self, user: User):
        res = self.user_service.create_user(user)

        if isinstance(res, UserServiceExtraError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, UserServiceError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            create_user_response = jsonable_encoder(CreateUserResponse(
                message=f"user was successfully created",
                user=user
            ))
            return JSONResponse(content=create_user_response, status_code=200, media_type="application/json")

    def update_user(self, user: User):
        res = self.user_service.update_user(user)
        if isinstance(res, UserServiceExtraError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, UserServiceError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            update_user_response = jsonable_encoder(UpdateUserResponse(
                message="user updated",
                user=res
            ))
            return JSONResponse(content=update_user_response, status_code=200, media_type="application/json")

    def update_user_description(self, update_user_description_body: UpdateUserDescriptionBody):
        user_id = update_user_description_body.user_id
        description = update_user_description_body.description
        res = self.user_service.update_user_description(user_id, description)
        if isinstance(res, UserServiceExtraError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, UserServiceError):
            content = jsonable_encoder(FindUserByProviderResponse(
                message=f"{res.name}: {res.message}",
                user=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            update_user_description_response = jsonable_encoder(UpdateUserDescriptionResponse(
                message="user description updated",
                user=res
            ))
            return JSONResponse(content=update_user_description_response, status_code=200, media_type="application/json")