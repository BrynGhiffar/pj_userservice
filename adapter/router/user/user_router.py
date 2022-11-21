from fastapi import APIRouter, Body
from domain.user.user_entity import User
from adapter.router.user.example.find_user_by_provider_example import FIND_USER_BY_PROVIDER_RESPONSE_EXAMPLE
from adapter.router.user.example.find_user_by_id_example import FIND_USER_BY_ID_RESPONSE_EXAMPLE
from adapter.router.user.example.update_user_description_example import UPDATE_USER_DESCRIPTION_EXAMPLE
from adapter.router.user.example.create_user_example import CREATE_USER_RESPONSE_EXAMPLE
from adapter.router.user.example.update_user_example import *
from adapter.router.user.user_handler import CreateUserResponse, UpdateUserResponse, UpdateUserDescriptionBody, UserHandler
from domain.user.user_service import UserService
from adapter.repository.user_repository import UserRepository
from adapter.repository.config import get_database

router = APIRouter()
user_handler = UserHandler(
    user_service=UserService(
        user_repository=UserRepository(
            user_repository_config=lambda: get_database()["user"]
        )
    )
)

@router.get(
    "/{user_id}",
    response_model=User,
    responses={
        200: {
            "description": "returned when user is found",
            "content": {
                "application/json": {
                    "example": FIND_USER_BY_ID_RESPONSE_EXAMPLE
                }
            }
        }
    }
)
def find_user_by_id(user_id: str):
    return user_handler.find_user_by_id(user_id)

@router.get(
    "/{provider}/{provider_id}",
    response_model=User,
    responses={
        200: {
            "description": "returned when all users with the given provider is found",
            "content": {
                "application/json": {
                    "example": FIND_USER_BY_PROVIDER_RESPONSE_EXAMPLE
                }
            }
        }
    }
)
def find_user_by_provider(provider: str, provider_id: str):
    return user_handler.find_user_by_provider(provider, provider_id)

@router.post(
    "/",
    response_model=CreateUserResponse,
    responses={
        200: {
            "description": "returned when all users with the given provider is found",
            "content": {
                "application/json": {
                    "example": CREATE_USER_RESPONSE_EXAMPLE
                }
            }
        }
    }
)
def create_user(user: User):
    return user_handler.create_user(user)

@router.put(
    "/",
    response_model=UpdateUserResponse,
    responses={
        200: {
            "description": "returned when the user details are updated",
            "content": {
                "application/json": {
                    "example": UPDATE_USER_RESPONSE_EXAMPLE
                }
            }
        }
    }
)
def update_user(user: User = Body(example=UPDATE_USER_BODY_EXAMPLE)):
    return user_handler.update_user(user)

@router.put(
    "/description",
    response_model=UpdateUserDescriptionBody,
    responses={
        200: {
            "description": "returned when the user description are updated",
            "content": {
                "application/json": {
                    "example": UPDATE_USER_DESCRIPTION_EXAMPLE
                }
            }
        }
    }

)
def update_user_description(update_user_description_body: UpdateUserDescriptionBody):
    return user_handler.update_user_description(update_user_description_body)