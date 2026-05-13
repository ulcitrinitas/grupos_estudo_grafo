from neo4j import GraphDatabase

from classes.aluno import Aluno
from classes.curso import Curso
from classes.grupo_estudo import Grupo_Estudo


def testa_conn():
    # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "6grKSWQvHSXtwpqWWegu")
    DB = "neo4j"

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            driver.verify_connectivity()
            print("conectado com sucesso")

            return {"uri": URI, "auth": AUTH, "db": DB}
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
                database_=db_auth["db"],
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
                database_=db_auth["db"],
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
                database_=db_auth["db"],
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
                database_=db_auth["db"],
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

def mostrar_aluno_grupo_grafo(db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                    MATCH (a:Aluno)-[p:PARTICIPA_DE]->(g:GrupoEstudo)
                    RETURN a.nome AS aluno_nome, a.email AS email, p.data_participacao AS data_participacao, collect(g.nome) AS grupos;
                """,
                database_=db_auth["db"],
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

            
def procurar_participantes(nome_grupo: str, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                    MATCH (a:Aluno)-[:PARTICIPA_DE]->(g:GrupoEstudo)
                    WHERE g.nome = $nome_grupo
                    RETURN g.nome AS grupo, collect(a.nome) AS alunos
                """,
                nome_grupo=nome_grupo,
                database_=db_auth["db"],
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

