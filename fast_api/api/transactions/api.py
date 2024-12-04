import psycopg2
from datetime import datetime
from fastapi import FastAPI, APIRouter, Query
import settings

transaction_route = APIRouter()


@transaction_route.get('/transactions')
async def transactions_list(date: str = Query(...)):
    
    connection = psycopg2.connect(settings.DB_URL)
    month_year = datetime.strptime(date, "%m-%Y")
    month = month_year.month
    year = month_year.year
    cursor = connection.cursor()

    select_query = """
    SELECT 
        id,
        date,
        client_id,
        card_id,
        amount,
        merchant_id,
        merchant_city,
        merchant_state,
        zip,
        use_chip
    FROM transactions
    WHERE EXTRACT(year FROM date) = %s
    AND EXTRACT(month FROM date) = %s;
    """
    cursor.execute(select_query, (year, month))
    result = cursor.fetchall()
    for row in result:
        print(row)
    return {"HAHAHA": "HAHAHAHA"}
