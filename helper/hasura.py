import requests, os
from dotenv import load_dotenv

load_dotenv('.env')
HASURA_HEADER = {'x-hasura-admin-secret': os.getenv('HASURA_HEADER')}

def hasura(query, variables):
    return requests.post(os.getenv('HASURA_SERVER'), headers=HASURA_HEADER, json={'query': query, 'variables': variables}).json()
    