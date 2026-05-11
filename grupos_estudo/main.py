from pprint import pprint

from database import testa_conn, insert_query, query_graph
from classes.person import Person_Data

db_auth = testa_conn()

p = Person_Data.model_validate({"name": "Alice", "friendname": "Bob"})

pprint(p)
print("--------------------------------------------------------------------------")
insert_query(p, db_auth)
print("--------------------------------------------------------------------------")
query_graph(db_auth)
