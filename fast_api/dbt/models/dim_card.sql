{{ config(materialized='incremental') }}

SELECT
    id,
    client_id,
    card_brand,
    card_type,
    card_number,
    expires,
    has_chip,
    num_cards_issued,
    credit_limit
FROM {{ source('public', 'cards_data') }}