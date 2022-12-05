from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from adapter.router.user import user_router as user
from dotenv import load_dotenv

import datetime
import os

load_dotenv()
USER_BASE_PATH = os.getenv("BASE_PATH")
VERSION_1 = os.getenv("VERSION_1")
FE_URL = os.getenv("FE_URL")

app = FastAPI()
app.include_router(
    user.router,
    prefix=f"{USER_BASE_PATH}{VERSION_1}",
)

origins = [
    FE_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectResponse(BaseModel):
    project_id: str
    name: str
    semester: str
    subject: str


class UserProjectResponse(BaseModel):
    user_id: str
    projects: List[ProjectResponse]

@app.get("/")
def read_root():
    now = datetime.datetime.now()
    return f"[{str(now)}] user_service is ok"

@app.get(
        "/user_service/projects/{user_id}",
        response_model=UserProjectResponse,
        responses={
            200: {
                "description": "returned when user is found",
                "content": {
                    "application/json": {
                        "example": {
                            "user_id": "123",
                            "projects": [
                                {
                                    "project_id": "prj-1234",
                                    "name": "DankChatApp0",
                                    "semester": "5",
                                    "subject": "Caterina"
                                },
                                {
                                    "project_id": "prj-1234",
                                    "name": "DankChatApp0",
                                    "semester": "5",
                                    "subject": "Caterina"
                                },
                                {
                                    "project_id": "prj-1234",
                                    "name": "DankChatApp0",
                                    "semester": "5",
                                    "subject": "Caterina"
                                },
                            ]
                        }
                    }
                }
            }
        }
    )
def get_user_projects(user_id: str):
    return {
        "user_id": user_id,
        "projects": [
            {
                "project_id": "prj-1234",
                "name": "DankChatApp0",
                "semester": "5",
                "subject": "Caterina"
            },
            {
                "project_id": "prj-1234",
                "name": "DankChatApp0",
                "semester": "5",
                "subject": "Caterina"
            },
            {
                "project_id": "prj-1234",
                "name": "DankChatApp0",
                "semester": "5",
                "subject": "Caterina"
            },
        ]
    }
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User Service",
        version="1.0.0",
        description="Schema for the user service",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)