# Dokumentasi Spark

Spark pada project ini bertugas dalam melakukan transform data yang diambil dari minIO dengan format .parquet. Pada tahap tranform ini dilakukan proses mengisi data yang kosong terutama pada merchant jika transaksinya online, menyesuaikan type data yang masuk kedalam bentuk schema. menghilangkan beberapa atribut yang tidak sesuai.

untuk struktur foldernya:
```
 dockers
│   ├── Dockerfile.spark
│   └── docker-compose-spark.yml
├── logs
│   ├── README.md
│   ├── hsperfdata_root
│   ├── hsperfdata_spark
│   │   ├── 41
│   │   └── 43
│   ├── spark-8b53e08c-8580-466a-93dd-c26b2e407c50  [error opening dir]
│   └── spark-f976a916-e100-4754-a9a8-f754c9a2718f  [error opening dir]
└── scripts
    ├── __init__.py
    ├── __pycache__
    │   └── base.cpython-39.pyc
    ├── base.py
    ├── cards_transform.py
    ├── transactions_transform.py
    └── users_transform.py

```

pastikan agar membuat folder `logs` agar tidak ada masalah dikemudian hari.
Cara membuat folder `logs`
1. pastikan current position terminal berada didalam spark
2. jalanakan `mkdir logs`
3. pastika folder `logs` memiliki akses terbuka agar ketika menjalankan airflow tidak ada error