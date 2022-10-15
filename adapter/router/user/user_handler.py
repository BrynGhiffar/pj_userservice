from domain.user import user_service
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from domain.user.user_entity import User
from domain.user.user_service import Error, UserNotFoundError, EmailAlreadyExistsError, ProviderIdAlreadyExistsError

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


def find_user_by_id(user_id: str):
    res = user_service.find_user_by_id(user_id)
    if not res:
        find_user_by_id_response = jsonable_encoder(FindUserByIdResponse(
            message="user not found"
        ))
        return JSONResponse(content=find_user_by_id_response, status_code=404, media_type="application/json")
    else:
        find_user_by_id_response = jsonable_encoder(FindUserByIdResponse(
            message="user found",
            user=res
        ))
        return JSONResponse(content=find_user_by_id_response, status_code=200, media_type="application/json")

def find_user_by_provider(provider: str, provider_id: str):
    res = user_service.find_user_by_provider_id(provider, provider_id)
    if not res:
        find_user_by_provider = jsonable_encoder(FindUserByProviderResponse(
            message="user not found",
        ))
        return JSONResponse(content=find_user_by_provider, status_code=404, media_type="application/json")
    else:
        find_user_by_provider = jsonable_encoder(FindUserByProviderResponse(
            message="user found",
            user=res
        ))
        return JSONResponse(content=find_user_by_provider, status_code=200, media_type="application/json")
    
def create_user(user: User):
    res = user_service.create_user(user)

    if not res:
        create_user_response = jsonable_encoder(CreateUserResponse(
            message="user already exists",
        ))
        return JSONResponse(content=create_user_response, status_code=400)
    else:
        create_user_response = jsonable_encoder(CreateUserResponse(
            message=f"user was successfully created",
            user=user
        ))
        return JSONResponse(content=create_user_response, status_code=200, media_type="application/json")

def update_user(user: User):
    res = user_service.update_user(user)
    if isinstance(res, Error):
        if (isinstance(res, UserNotFoundError)):
            update_user_response = jsonable_encoder(UpdateUserResponse(
                message="cannot update, user not found"
            ))
            return JSONResponse(content=update_user_response, status_code=404, media_type="application/json")
        elif isinstance(res, ProviderIdAlreadyExistsError):
            update_user_response = jsonable_encoder(UpdateUserResponse(
                message="cannot update, provider id already exists"
            ))
            return JSONResponse(content=update_user_response, status_code=400, media_type="application/json")
        elif isinstance(res, EmailAlreadyExistsError):
            update_user_response = jsonable_encoder(UpdateUserResponse(
                message="cannot update, email already exists"
            ))
            return JSONResponse(content=update_user_response, status_code=400, media_type="application/json")
    else:
        update_user_response = jsonable_encoder(UpdateUserResponse(
            message="user updated",
            user=res
        ))
        return JSONResponse(content=update_user_response, status_code=200, media_type="application/json")

def update_user_description(update_user_description_body: UpdateUserDescriptionBody):
    user_id = update_user_description_body.user_id
    description = update_user_description_body.description
    updated_res = user_service.update_user_description(user_id, description)
    if not updated_res:
        update_user_description_response = jsonable_encoder(UpdateUserDescriptionResponse(
            message="user not found"
        ))
        return JSONResponse(content=update_user_description_response, status_code=404, media_type="application/json")
    else:
        update_user_description_response = jsonable_encoder(UpdateUserDescriptionResponse(
            message="user description updated",
            user=updated_res
        ))
        return JSONResponse(content=update_user_description_response, status_code=200, media_type="application/json")