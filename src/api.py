"""
This is the main api fie where all the routes are
provided
"""
from fastapi import FastAPI
from src.v1.routers import retriever_route
from src.v1.routers import generator_route

def create_app():
    """
    API app creation function
    """
    app_ = FastAPI()

    #Include the routes
    app_.include_router(generator_route.router, prefix="/api/v1")
    app_.include_router(retriever_route.router, prefix="/api/v1")

    return app_

app = create_app()
