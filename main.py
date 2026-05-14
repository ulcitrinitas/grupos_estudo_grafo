from fastapi import FastAPI

from classes.aluno import Aluno
from classes.curso import Curso

# db_auth = testa_conn()

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "Foo": "Bar"
    }
    

app.get("/curso")
def mostrar_aluno():
    
    curso = Curso.model_validate({"nome": "IA", "duraçao": 8})
    return curso.model_dump_json()
