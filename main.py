from fastapi import FastAPI

from pprint import pprint

from classes.aluno import Aluno
from classes.curso import Curso

from neo4j_querys import testa_conn, mostrar_aluno_grupo_grafo

db_auth = testa_conn()

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "Foo": "Bar"
    }
    

@app.get("/participantes")
def mostrar_participantes():
    registros = mostrar_aluno_grupo_grafo(db_auth)
    return registros
