"""This is the schema for the user profile"""
from typing import List
from pydantic import BaseModel

class SocialMeadia(BaseModel):
    """This is the schema for the user social media"""
    name: str
    link: str

class Profile(BaseModel):
    """This is the schema for the user profile"""
    fullName: str
    email: str
    phoneNumber: str
    socialMedia: List[SocialMeadia]
    