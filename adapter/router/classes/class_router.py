from fastapi import APIRouter, Body
from domain.classes.class_entity import Class
from adapter.router.user.example.find_user_by_provider_example import FIND_USER_BY_PROVIDER_RESPONSE_EXAMPLE
from adapter.router.user.example.find_user_by_id_example import FIND_USER_BY_ID_RESPONSE_EXAMPLE
from adapter.router.user.example.update_user_description_example import UPDATE_USER_DESCRIPTION_EXAMPLE
from adapter.router.user.example.create_user_example import CREATE_USER_RESPONSE_EXAMPLE
from adapter.router.user.example.find_all_user_example import FIND_ALL_USER_EXAMPLE
from adapter.router.user.example.update_user_example import *
from adapter.router.classes.class_handler import CreateClassResponse, UpdateClassResponse, ClassHandler
from domain.classes.class_service import ClassService
from domain.notification.notification_service import NotificationService
from adapter.repository.class_repository import ClassRepository
from adapter.repository.config import get_database
from adapter.discord.api import DiscordApi
from adapter.discord.config import get_webhook

router = APIRouter()
class_handler = ClassHandler(
    classes_service=ClassService(
        class_repository=ClassRepository(
           classes_repository_config=lambda: get_database()["class"]
        ),
        notification_service=NotificationService(
            api=DiscordApi(
                webhook_url=get_webhook()
            )
        )
    )
)

@router.get(
    "/{class_id}",
    response_model=Class,
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
def find_class_by_id(class_id: str):
    return class_handler.find_classes_by_id(class_id)

@router.get(
    "/",
    response_model=list[Class],
    responses={
        200: {
            "description": "returns all users in the database",
            "content": {
                "application/json": {
                    "example": FIND_ALL_USER_EXAMPLE
                }
            }
        }
    }
)

# Need bug fixing
# def find_all_classes():
#     return class_handler.find_all_classes()

# @router.post(
#     "/",
#     response_model=CreateClassResponse,
#     responses={
#         200: {
#             "description": "returned when all users with the given provider is found",
#             "content": {
#                 "application/json": {
#                     "example": CREATE_USER_RESPONSE_EXAMPLE
#                 }
#             }
#         }
#     }
# )
def create_class(classes: Class):
    return class_handler.create_classes(classes)

@router.put(
    "/",
    response_model=UpdateClassResponse,
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
def update_class(classes: Class = Body(example=UPDATE_USER_BODY_EXAMPLE)):
    return class_handler.update_classes(classes)

# Just In Case For Future 
# @router.get("/user/")
# def find_user_by_name(name: str):
#     return user_handler.find_user_by_name(name)