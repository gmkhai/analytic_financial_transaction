{{ config(materialized='incremental') }}

SELECT 
    DISTINCT(merchant_id) as id,
    merchant_city,
    merchant_state,
    zip
FROM {{ source('public', 'transactions_data') }}