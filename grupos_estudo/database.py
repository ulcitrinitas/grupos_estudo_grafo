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
        except Exception:
            print("conexão falhou")


def insert_query(data: Person_Data, db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            summary = driver.execute_query(
                """
                    CREATE (a:Person {name: $name})
                    CREATE (b:Person {name: $friendName})
                    CREATE (a)-[:KNOWS]->(b)
            """,
                name=data.name,
                friendName=data.friendname,
                database_="neo4j",
            ).summary

            print(f"CREATED ({data.name})-[:KNOWS]->({data.friendname})")

            print(
                "Created {nodes_created} nodes in {time} ms.".format(
                    nodes_created=summary.counters.nodes_created,
                    time=summary.result_available_after,
                )
            )
        except Exception:
            print("Erro ao inserir os dados")


def query_graph(db_auth):
    with GraphDatabase.driver(db_auth["uri"], auth=db_auth["auth"]) as driver:
        try:
            records, summary, keys = driver.execute_query(
                """
                MATCH (a:Aluno)-[:PARTICIPA_DE]->(g:GrupoEstudo)
                RETURN a.nome, collect(g.nome) AS grupos
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
        except Exception:
            print("Erro ao pegar o grafo")
