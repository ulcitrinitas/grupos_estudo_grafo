from pprint import pprint

from database import testa_conn
from person import Person_Data

db_auth = testa_conn()

p = Person_Data.model_validate({"name": "Alice", "friendname": "Bob"})

pprint(p)