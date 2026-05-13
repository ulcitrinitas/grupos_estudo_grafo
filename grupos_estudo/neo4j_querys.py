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

# Funções para criar os nós do grafo

def criar_aluno(aluno: Aluno, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    MERGE (a:Aluno {matricula: $matricula})
                    ON CREATE SET a.nome = $nome_aluno, a.email = $email, a.idade = $idade;
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
                    MERGE (c:Curso {nome: $nome_curso})
                    ON CREATE SET c.duracao = $duracao;
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

def criar_grupo(grupo: Grupo_Estudo, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    MERGE (g:GrupoEstudo {data_criacao: datetime()})
                    ON CREATE
                    SET g.nome = $nome_grupo
                    RETURN g.nome, g.data_criacao;
                    """,
                nome_grupo=grupo.nome,
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


# Funções para criar relacionamentos

def criar_no_aluno_curso(aluno: Aluno, curso: Curso, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    MATCH (a:Aluno {matricula: $matricula}), (c:Curso {nome: $nome_curso})
                    MERGE (a)-[:MATRICULADO_EM]->(c);
                """,
                matricula=aluno.matricula,
                nome_curso=curso.nome,
                database_="neo4j",
            ).summary

            print(
                "Created {relationships_created} relationships in {time} ms.".format(
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

            
def criar_relacao_aluno_grupo(aluno: Aluno, grupo: Grupo_Estudo, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    MATCH (a:Aluno {matricula: $matricula}), (g:GrupoEstudo {nome: $nome_grupo})
                    MERGE (a)-[:PARTICIPA_DE {data_participacao: datetime()}]->(g);
                """,
                matricula=aluno.matricula,
                nome_grupo=grupo.nome,
                database_="neo4j",
            ).summary

            print(
                "Created {relationships_created} relationships in {time} ms.".format(
                    relationships_created=summary.counters.relationships_created,
                    time=summary.result_available_after,
                )
            )

            print(
                f"CREATED ({aluno.nome}:Aluno)-[:PARTICIPA_DE]->({grupo.nome}:Curso)"
            )
        except Exception as e:
            print("Erro ao inserir os dados")
            print(f"Mensagem de erro {e}")

# Funções para mostrar as relações

def mostrar_aluno_curso_grafo(db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                    MATCH (a:Aluno)-[:MATRICULADO_EM]->(c:Curso)
                    RETURN a.nome AS aluno_nome, a.email AS email, c.nome AS curso_nome;
                """,
                database_="neo4j",
            )
            for record in records:
                print(record.data())

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

# Funções para procurar os campos no grafo

def procurar_aluno_curso(nome_curso: str, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                    MATCH (a:Aluno)-[:MATRICULADO_EM]->(c:Curso)
                    WHERE c.nome = $nome_curso
                    RETURN a.nome AS aluno_nome, a.email AS aluno_email, c.nome AS curso_nome;
                """,
                nome_curso=nome_curso,
                database_="neo4j",
            )
            for record in records:
                print(record.data())

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
