import requests
import os
from dotenv import load_dotenv
from pathlib import Path

def load_card_transaction():
    path_envfile = Path('/opt/.env')
    load_dotenv(path_envfile)

    # load variable from .env
    FASTAPI_HOST = os.getenv('FASTAPI_CONTAINER_NAME')
    FASTAPI_PORT = os.getenv('FASTAPI_PORT')
    
    response = requests.get(f'http://{FASTAPI_HOST}:{FASTAPI_PORT}/hit-dbt?unique_command=project_akhir_dbt')
    response_result = response.json()
    if response_result.get("status_code") == 200:
        print(f"PUSH DATA TRANSACTIONS TO USING DBT SUCCESS!!!")
    else:
        print(f"PUSH DATA TRANSACTIONS TO USING DBT SUCCESS!!!")
