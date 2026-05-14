from pydantic import BaseModel, EmailStr, PositiveInt


class Aluno(BaseModel):
    nome: str
    matricula: PositiveInt
    email: EmailStr
    idade: PositiveInt
