# You can add all configuration API in this file

import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../.env')
load_dotenv(dotenv_path)

POSTGRES_CONTAINER_NAME = os.getenv('POSTGRES_CONTAINER_NAME')
POSTGRES_DB_API = os.getenv('POSTGRES_DB_API')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_CONTAINER_NAME}:{POSTGRES_PORT}/{POSTGRES_DB_API}"