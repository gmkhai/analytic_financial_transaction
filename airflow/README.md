# Dokumentasi Airflow

Airflow merupakan orchestration yang digunakan untuk mengalirkan data dari berbagai sumber ke datawarehouse. Pada airflow ini proses ETL akan di jadwalkan dan di alirkan dalam bentuk task dengan proses extraction mengambil data dari 2 jenis sumber data yaitu `API` dan `Database` untuk memahami konsep dari `Ingestion` data dari berbagai sumber.

**Struktur Folder**

```
├── README.md
├── commands
│   └── entrypoint.sh
├── dags
│   ├── __init__.py
│   ├── extract_dag.py
│   ├── load_dag.py
│   ├── main_dag.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── extracts
│   │   │   ├── __init__.py
│   │   │   └── card_transaction.py
│   │   ├── loads
│   │   │   ├── __init__.py
│   │   │   └── card_transaction.py
│   │   └── transforms
│   │       └── __init__.py
│   └── transform_dag.py
├── dockers
│   ├── Dockerfile.airflow
│   └── docker-compose-airflow.yml
└── logs
```

Untuk menjalankan docker dari airflow ini struktur folder ini harus lengkap.

**Note**
jika sudah melakukan clone di repository ini folder logsnya tidak ada silahkan dibuat terlebih dahulu sebelum 
create image

Cara membuat folder `logs`
1. pastikan current position terminal berada didalam airflow
2. jalanakan `mkdir logs`
3. pastika folder `logs` memiliki akses terbuka agar ketika menjalankan airflow tidak ada error