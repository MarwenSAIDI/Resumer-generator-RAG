"""
The retriever route file
"""
from fastapi import APIRouter, status

router = APIRouter()

@router.get("/status")
def status():
    return {"status": status.HTTP_200_OK}