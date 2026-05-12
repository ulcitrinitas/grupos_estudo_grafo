from pprint import pprint

from neo4j_querys import testa_conn, criar_aluno, criar_curso, criar_no_aluno_curso, mostrar_aluno_curso_grafo 
from classes.aluno import Aluno
from classes.curso import Curso

db_auth = testa_conn()

a = Aluno.model_validate(
    {
        "nome": "Lilia Głowacka",
        "matricula": 85236,
        "email": "lilia_głowacka@email.com",
        "idade": 26,
    }
)

c = Curso.model_validate({"nome": "Ciência da Computação", "duraçao": 8})

print("---------------------------------------------------")

print("---------------------------------------------------")

print("---------------------------------------------------")

