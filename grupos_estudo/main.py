from pprint import pprint

from database import testa_conn

db_auth = testa_conn()

pprint(db_auth)
