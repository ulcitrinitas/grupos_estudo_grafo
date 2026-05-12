from pprint import pprint

from database import testa_conn, insert_aluno_curso, query_aluno_curso_graph
from classes.aluno import Aluno
from classes.curso import Curso

db_auth = testa_conn()

a = Aluno.model_validate(
    {
        "nome": "Ana Pereira",
        "matricula": 74128,
        "email": "ana_pereira@email.com",
        "idade": 24,
    }
)

c = Curso.model_validate({"nome": "Inteligência Artificial", "duraçao": 8})

print("---------------------------------------------------")
pprint(a)
pprint(c)
print("---------------------------------------------------")
insert_aluno_curso(a, c, db_auth)
print("---------------------------------------------------")
query_aluno_curso_graph(db_auth)
