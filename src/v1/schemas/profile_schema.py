from typing import List
from pydantic import BaseModel

class SocialMeadia(BaseModel):
    name: str
    link: str

class Profile(BaseModel):
    fullName: str
    email: str
    phoneNumber: str
    socialMedia: List[SocialMeadia]