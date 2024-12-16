# Dokumentasi FastAPI

API dengan FastAPI yang dibangun digunakan untuk mengambil data transaksi yang berjumlah 13++ juta data yang perlu disimpan. Untuk menggunakan service ini

1. Download file data di https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets.

2. create table sesuai dengan yang ada di .env file
    - create table data_cards
        ```
        CREATE TABLE public.cards (
        id int8 NOT NULL,
        client_id int8 NULL,
        card_brand varchar(30) NULL,
        card_type varchar(20) NULL,
        card_number varchar(100) NOT NULL,
        expires varchar(100) NOT NULL,
        cvv int4 NULL,
        has_chip bool NOT NULL,
        num_cards_issued int4 NULL,
        credit_limit varchar(200) NOT NULL,
        acct_open_date varchar(100) NULL,
        year_pin_last_changed int4 NULL,
        card_on_dark_web varchar(100) NULL,
        CONSTRAINT cards_pkey PRIMARY KEY (id)
        );
    - create table data_transactions
        ```
        CREATE TABLE public.transactions (
        id int8 NOT NULL,
        "date" date NULL,
        client_id int8 NOT NULL,
        card_id int8 NOT NULL,
        amount varchar(200) NOT NULL,
        merchant_id int8 NOT NULL,
        merchant_city varchar(200) NULL,
        merchant_state varchar(200) NULL,
        zip float8 NULL,
        use_chip varchar(50) NULL,
        mcc int4 NULL,
        errors varchar(400) NULL,
        CONSTRAINT transactions_pkey PRIMARY KEY (id)
        );
    
    - create table data_users
        ```
        CREATE TABLE public.users (
        id int8 NOT NULL,
        current_age int4 NOT NULL,
        retirement_age int4 NULL,
        birth_year int4 NOT NULL,
        birth_month int4 NOT NULL,
        gender varchar(20) NOT NULL,
        address varchar(200) NULL,
        latitude float8 NULL,
        longitude float8 NULL,
        per_capita_income varchar(100) NOT NULL,
        yearly_income varchar(100) NULL,
        total_debt varchar(100) NULL,
        credit_score int4 NULL,
        num_credit_cards int4 NULL,
        CONSTRAINT users_pkey PRIMARY KEY (id)
        );

3. Setelah schema dibuat import data yang sudah didownload kedalam database dengan manual. Bisa dengan DBeaver, TablePlus, atau lain sebagainya.
4. Ketika prosesnya sudah selesai jalankan `127.0.0.1:8000` ketika docker fastAPI sudah berjalan.


# Dokumentasi DBT

Pada folder ini untuk proses DBT akan dijalankan dengan menggunakan API dari FastAPI. Sebelum menjalankan docker compose atau image silahkan membuat folder baru dengan nama `logs` didalam folder `fast_api/dbt` setelah pembuatan file selesai silahkan jalankan docker image dan docker composenya. Penyebab kenapa DBT dijalankan di FastAPI karena ada kendala dalam menjalankan dbt didalam container airflow karena ada beberapa conflict dengan dependencies dari airflow dan dbt. Sehingga saya mencari alternatif lain adalah menjalankan DBT dengan API.