from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from domain.classes.class_entity import Class
from domain.classes.class_service import ClassServiceError, \
                                    ClassService, \
                                    ClassServiceExtraError

class CreateClassResponse(BaseModel):
    message: str
    classes: Class | None

class FindClassByIdResponse(BaseModel):
    message: str
    classes: Class | None

class UpdateClassResponse(BaseModel):
    message: str
    classes: Class | None

class FindAllClassResponse(BaseModel):
    message: str
    classes: list[Class] | None

class ClassHandler:
    def __init__(self, classes_service: ClassService):
        self.classes_service = classes_service

    def find_classes_by_id(self, classes_id: str):
        res = self.classes_service.find_class_by_id(classes_id)
        if isinstance(res, ClassServiceExtraError):
            content = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                classes=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, ClassServiceError):
            find_classes_by_id_response = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}",
                classes=None
            ))
            return JSONResponse(content=find_classes_by_id_response, status_code=404, media_type="application/json")
        else:
            find_classes_by_id_response = jsonable_encoder(FindClassByIdResponse(
                message="classes found",
                classes=res
            ))
            return JSONResponse(content=find_classes_by_id_response, status_code=200, media_type="application/json")
        
    def create_classes(self, classes: Class):
        res = self.classes_service.create_class(classes)

        if isinstance(res, ClassServiceExtraError):
            content = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                classes=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, ClassServiceError):
            content = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}",
                classes=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            create_classes_response = jsonable_encoder(CreateClassResponse(
                message=f"classes was successfully created",
                classes=classes
            ))
            return JSONResponse(content=create_classes_response, status_code=200, media_type="application/json")

    def update_classes(self, classes: Class):
        res = self.classes_service.update_classes(classes)
        if isinstance(res, ClassServiceExtraError):
            content = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                classes=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        elif isinstance(res, ClassServiceError):
            content = jsonable_encoder(FindClassByIdResponse(
                message=f"{res.name}: {res.message}",
                classes=None
            ))
            return JSONResponse(content=content, status_code=404, media_type="application/json")
        else:
            update_classes_response = jsonable_encoder(UpdateClassResponse(
                message="classes updated",
                classes=res
            ))
            return JSONResponse(content=update_classes_response, status_code=200, media_type="application/json")
    
    # Need bug fixing
    # def find_all_classes(self):
    #     res = self.classes_service.find_all_classes()
    #     if isinstance(res, ClassServiceExtraError):
    #         content = jsonable_encoder(FindAllClassResponse(
    #             message=f"{res.name}: {res.message}. {res.extra_message}",
    #             classess=None
    #         ))
    #         return JSONResponse(content=content, status_code=404, media_type="application/json")
    #     elif isinstance(res, ClassServiceError):
    #         content = jsonable_encoder(FindAllClassResponse(
    #             message=f"{res.name}: {res.message}",
    #             classess=None
    #         ))
    #         return JSONResponse(content=content, status_code=404, media_type="application/json")
    #     else:
    #         update_classes_description_response = jsonable_encoder(FindAllClassResponse(
    #             message="found all classess",
    #             classess=res
    #         ))
    #         return JSONResponse(content=update_classes_description_response, status_code=200, media_type="application/json")

    # Just In Case For Future 
    # def find_classes_by_name(self, name: str):
    #     res = self.classes_service.find_classes_by_name(name)
    #     if isinstance(res, ClassServiceExtraError):
    #         content = jsonable_encoder(FindAllClassResponse(
    #             message=f"{res.name}: {res.message}. {res.extra_message}",
    #             classess=None
    #         ))
    #         return JSONResponse(content=content, status_code=404, media_type="application/json")
    #     elif isinstance(res, ClassServiceError):
    #         content = jsonable_encoder(FindAllClassResponse(
    #             message=f"{res.name}: {res.message}",
    #             classess=None
    #         ))
    #         return JSONResponse(content=content, status_code=404, media_type="application/json")
    #     else:
    #         update_classes_description_response = jsonable_encoder(FindAllClassResponse(
    #             message="found all classess",
    #             classess=res
    #         ))
    #         return JSONResponse(content=update_classes_description_response, status_code=200, media_type="application/json")