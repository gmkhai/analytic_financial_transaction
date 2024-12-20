from fastapi import FastAPI
from transactions.api import transaction_route

app = FastAPI()

app.include_router(transaction_route)
