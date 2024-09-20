"""
This is the main api fie where all the routes are
provided
"""
from fastapi import FastAPI
from src.v1.routers import retrieverV1_route
from src.v1.routers import generatorV1_route

def create_app():
    """
    API app creation function
    """
    app_ = FastAPI()

    #Include the routes
    app_.include_router(generatorV1_route.router, prefix="/v1/generator")
    app_.include_router(retrieverV1_route.router, prefix="/v1/retriever")

    return app_

app = create_app()
