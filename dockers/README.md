# Dokumentasi Docker

Docker pada folder ini hanya berisi docker-compose yang menjadi tempat penyimpanan data diantaranya:
1. postgreSQL yang menjadi tempat penyimpanan data untuk fastAPI, selain itu di postgreSQL ini juga menjadi tempat penyimpanan data warehouse
2. minIO merupakan tempat penyimpanan berbasis object storage. Jadi data yang sudah di ingestion akan disimpan kedalam format .parquet di dalam bucket yang telah ditentukan

**Note**:
untuk menggunakan mimIO pastikan terlebih dalahulu membuat nama bucket sesuai yang diinginkan dan pastikan sama dengan bucket yang ada di file `airflow/dags/tasks/extracts/card_transaction.py` function `connection_save_to_minio`

untuk menjalankan service ini bisa dijalankan sekaligus dengan perintah `make docker-compose`.