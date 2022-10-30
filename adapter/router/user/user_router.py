from fastapi import APIRouter, Body
from domain.user.user_entity import User
from adapter.router.user import user_handler
from adapter.router.user.example.find_user_by_provider_example import FIND_USER_BY_PROVIDER_RESPONSE_EXAMPLE
from adapter.router.user.example.find_user_by_id_example import FIND_USER_BY_ID_RESPONSE_EXAMPLE
from adapter.router.user.example.update_user_example import *
from adapter.router.user.user_handler import CreateUserResponse, UpdateUserResponse, UpdateUserDescriptionBody
import datetime

router = APIRouter()

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
    "/description"
)
def update_user_description(update_user_description_body: UpdateUserDescriptionBody):
    return user_handler.update_user_description(update_user_description_body)