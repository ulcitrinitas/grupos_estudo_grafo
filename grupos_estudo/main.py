from pprint import pprint

from database import testa_conn, insert_query
from grupos_estudo.classes.person import Person_Data

db_auth = testa_conn()

p = Person_Data.model_validate({"name": "Alice", "friendname": "Bob"})

pprint(p)

insert_query(p, db_auth)
