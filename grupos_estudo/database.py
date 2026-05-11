from neo4j import GraphDatabase

from grupos_estudo.classes.person import Person_Data


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
            summary = driver.execute_query("""
                    CREATE (a:Person {name: $name})
                    CREATE (b:Person {name: $friendName})
                    CREATE (a)-[:KNOWS]->(b)
            """,
            name=data.name, friendName=data.friendname,
            database_= "neo4j").summary
            
            print(f"CREATED ({data.name})-[:KNOWS]->({data.friendname})")
            
            print(
                "Created {nodes_created} nodes in {time} ms.".format(
                    nodes_created=summary.counters.nodes_created,
                    time=summary.result_available_after,
                )
            )
        except Exception:
            ...
    ...
