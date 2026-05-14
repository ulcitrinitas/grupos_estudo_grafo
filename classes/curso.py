from pydantic import BaseModel, PositiveInt

class Curso(BaseModel):
    nome: str
    duraçao: PositiveInt
