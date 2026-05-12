from neo4j import GraphDatabase

from classes.aluno import Aluno
from classes.curso import Curso
from classes.grupo_estudo import Grupo_Estudo


def testa_conn():
    # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "6grKSWQvHSXtwpqWWegu")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            driver.verify_connectivity()
            print("conectado com sucesso")

            return {"uri": URI, "auth": AUTH}
        except Exception as e:
            print("conexão falhou")
            print(f"Mensagem de erro {e}")


def criar_aluno(aluno: Aluno, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    CREATE (:Aluno {nome: $nome_aluno, matricula: $matricula, email: $email, idade: $idade});
                """,
                nome_aluno=aluno.nome,
                matricula=aluno.matricula,
                email=aluno.email,
                idade=aluno.idade,
                database_="neo4j",
            ).summary

            print(
                "Created {nodes_created} nodes in {time} ms.".format(
                    nodes_created=summary.counters.nodes_created,
                    time=summary.result_available_after,
                )
            )
        except Exception as e:
            print("Erro ao inserir os dados")
            print(f"Mensagem de erro {e}")

def criar_curso(curso: Curso, db_auth):
        with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
            try:
                summary = driver.execute_query(
                    """
                        CREATE (:Curso {nome: $nome_curso, duracao: $duracao});
                    """,
                    nome_curso=curso.nome,
                    duracao=curso.duraçao,
                    database_="neo4j",
                ).summary

                print(
                    "Created {nodes_created} nodes in {time} ms.".format(
                        nodes_created=summary.counters.nodes_created,
                        time=summary.result_available_after,
                    )
                )
            except Exception as e:
                print("Erro ao inserir os dados")
                print(f"Mensagem de erro {e}")


def criar_no_aluno_curso(aluno: Aluno, curso: Curso, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    MATCH (a:Aluno {matricula: $matricula}), (c:Curso {nome: $nome_curso})
                    CREATE (a)-[:MATRICULADO_EM]->(c)
                """,
                matricula=aluno.matricula,
                nome_curso=curso.nome,
                database_="neo4j",
            ).summary

            print(
                "Created {relationships_created} nodes in {time} ms.".format(
                    relationships_created=summary.counters.relationships_created,
                    time=summary.result_available_after,
                )
            )

            print(
                f"CREATED ({aluno.nome}:Aluno)-[:MATRICULADO_EM]->({curso.nome}:Curso)"
            )
        except Exception as e:
            print("Erro ao inserir os dados")
            print(f"Mensagem de erro {e}")


def mostrar_aluno_curso_grafo(db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                    MATCH (a:Aluno)-[:MATRICULADO_EM]->(c:Curso)
                    RETURN a.nome, a.matricula, a.email, c.nome AS curso
                """,
                database_="neo4j",
            )
            for record in records:
                print(record.data())
                print(record.data())  # obtain record as dict

            # Summary information
            print(
                "The query `{query}` returned {records_count} records in {time} ms.".format(
                    query=summary.query,
                    records_count=len(records),
                    time=summary.result_available_after,
                )
            )
        except Exception as e:
            print("Erro ao pegar o grafo")
            print(f"Mensagem de erro {e}")
