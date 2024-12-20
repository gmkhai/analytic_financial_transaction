import psycopg2
import settings
from datetime import datetime
from fastapi import APIRouter,HTTPException, Query, status
from transactions.utils import run_dbt_command

transaction_route = APIRouter()


@transaction_route.get('/transactions')
async def transactions_list(date: str = Query(...)):
    """
    API for get transactions card by month years
    :param date: str 12-2020
    :return response: dict
    """
    response = {
        "message": "You have problem when get data card transaction",
        "status_code": status.HTTP_400_BAD_REQUEST,
        "result": None
    }

    # initialize variable postgres and get parameters query
    connection = psycopg2.connect(settings.DB_URL)
    month_year = datetime.strptime(date, "%m-%Y")
    month = month_year.month
    year = month_year.year
    cursor = connection.cursor()

    # set query for result
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
    AND EXTRACT(month FROM date) = %s
    ORDER BY date ASC;
    """
    cursor.execute(select_query, (year, month))
    results = cursor.fetchall()

    # mapping result data
    if results:
        row_datas = []
        for row in results:
            data = {
                "id": row[0],
                "date": row[1],
                "client_id": row[2],
                "card_id": row[3],
                "amount": row[4],
                "merchant_id": row[5],
                "merchant_city": row[6],
                "merchant_state": row[7],
                "zip": row[8],
                "use_chip": row[9],
            }
            row_datas.append(data)
        response["result"] = row_datas
        response["status_code"] = status.HTTP_200_OK
        response["message"] = "Retrieve data card transaction success"
    else:
        response["message"] = f"Data transaction card not found for {date}"
        response["status_code"] = status.HTTP_404_NOT_FOUND
    return response


@transaction_route.get('/hit-dbt')
async def running_dbt_process(unique_command: str = Query()):
    """
    API for hit dbt run
    :param unique_command: str hard code manual using this 'project_akhir_dbt'
    :return response: dict
    """
    if unique_command != 'project_akhir_dbt':
        raise HTTPException(status_code=400, detail=f"Invalid command: {unique_command}")
    
    command = "run"
    result = run_dbt_command(command)
    return {"command": command, "output": result, "status_code": 200}