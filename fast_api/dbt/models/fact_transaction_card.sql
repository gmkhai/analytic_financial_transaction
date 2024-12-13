{{ config(materialized='incremental') }}

SELECT
    id,
    date,
    client_id AS user_id,
    card_id,
    merchant_id,
    amount
FROM {{ source('public', 'transactions_data') }}