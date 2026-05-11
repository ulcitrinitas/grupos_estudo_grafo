from pydantic import BaseModel

class Person_Data(BaseModel):
    name: str
    friendname: str