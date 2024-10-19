"""
This is the main api fie where all the routes are
provided
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from typing import Callable
from src.v1.routers import retriever_route
from src.v1.routers import generator_route
from src.v1.utils.logger import logger
from src.exceptions import *
from src.config import config

TITLE=config['DEFAULT']['name']
VERSION=config['DEFAULT']['version']

def create_exception_handler(
        status_code: int, initial_detail: str
) -> Callable[[Request, ResumerGeneratorApiError], JSONResponse]:
    detail = {"message": initial_detail}

    async def exception_handler(
        _: Request, 
        exc: ResumerGeneratorApiError
    ) -> JSONResponse:
        if exc.message:
            detail['message'] = exc.message
        
        if exc.name:
            detail['message'] = f"{detail['message']} [{exc.name}]"

        logger.error(exc)
        return JSONResponse(
            status_code=status_code, content={'detail': detail['message']}
        )
    
    return exception_handler

def create_app():
    """
    API app creation function
    """
    app_ = FastAPI(title=TITLE, version=VERSION)

    # Include the routes
    app_.include_router(generator_route.router, prefix="/api/v1")
    app_.include_router(retriever_route.router, prefix="/api/v1")

    # Add exceptions
    app_.add_exception_handler(
        exc_class_or_status_code=ServiceError,
        handler=create_exception_handler(
            status.HTTP_404_NOT_FOUND, "Service does not respond"
        ),
    )

    app_.add_exception_handler(
        exc_class_or_status_code=EntityDoesNotExistError,
        handler=create_exception_handler(
            status.HTTP_404_NOT_FOUND, "Entity does not exist"
        ),
    )

    app_.add_exception_handler(
        exc_class_or_status_code=UnprocessedRequestError,
        handler=create_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Third-party request did not function properly"
        ),
    )

    return app_

app = create_app()
