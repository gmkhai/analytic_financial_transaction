{{ config(materialized='incremental') }}

SELECT
    id,
    current_age,
    retirement_age,
    birth_year,
    birth_month,
    gender,
    per_capita_income,
    yearly_income,
    total_debt,
    credit_score,
    num_credit_cards
FROM {{ source('public', 'users_data') }}