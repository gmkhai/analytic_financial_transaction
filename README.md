# Introduction

Proyek ini bertujuan untuk merancang pipeline ETL (Extract, Transform, Load) untuk menganalisis perilaku pelanggan saat menggunakan kartu kredit. Tujuan proyek ini adalah agar tim marketing dapat memberikan diskon atau promo kepada pelanggan yang bertransaksi di merchant yang menjadi mitra layanan kartu kredit. Hasil dari proyek ini adalah data analisis yang memberikan ringkasan mengenai merchant dengan jumlah transaksi yang sedikit di setiap kota.

# Project Overview
Melakukan otomatisasi untuk beberapa tahap dari tahap extraction hingga di simpan ke load datawarehouse dengan memperhatikan kebutuhan data dari subject. Kemudian data tersebut menjadi bahan untuk menentukan keputusan bisnis terkait dengan penggunaan kartu kredit

# Architecture Diagram
![alt text](<documentions/ETL Architecture Muhammad Khairunnas.png>)

# Tools and Technologies Used
**1. FastAPI**

Framework yang digunakan untuk mengambangkan API yang menjadi sumber data yang ingin ingest. Framework ini dikembangkan dengan menggunakan bahasa python. 

**2. PostgreSQL**

Database yang menjadi sumber data untuk di ingestion sekaligus sebagai tempat datawarehouse sebelum dianalisis oleh subject. Database ini berbasis RDBMS yang memiliki relasi untuk setiap tablenya.

**3. MinIO**

Data storage yang menjadi tempat landing data setelah di-ingestion. data yang sudah di-ingest akan disimpan kedalam format parquet.

**4. Spark**

Layanan untuk melakukan transformasi data pada project ini adalah spark atau lebih tepatnya pyspark. pada project ini digunakan spark cluster dengan 2 node karena memerlukan proses data yang cukup banyak.

**5. DBT**

Platform yang digunakan untuk melakukan data modeling adalah DBT pada tahap ini dilakukan filtering data yang ingin di-create di data warehouse sebagai datamart untuk membatasi akses beberapa data yang akan digunakan oleh subject.

**6. Airflow**

Platform orchestration untuk menjalankan proses ETL secara terjadwal. Platform ini sangat berguna untuk proses design alur ETL karena digunakan untuk tugas yang fleksibel dan kompleks.

**6. PowerBI**

Platform yang terakhir yang digunakan adalah power BI. Platform ini digunakan untuk visualisasi data dari data yang sudah di query dari data mart.


# Dataset Description
Dataset yang digunakan adalah dataset dari kaggle Financial Transactions Dataset  Analytics dari link berikut https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets, data yang diambil sebanyak 3 data masing-masing adalah:

1. cards_data.csv (6146 record)

    merupakan data yang berisi informasi dari kartu yang digunakan untuk transaksi termasuk users/ clients yang menggunakan kartu tersebut.terdiri dari kolom:

    ```
    id : type biginteger, sebagai primary key
    client_id big integer, sebagai foreign key yang terhubung dengan data users_data.csv
    card_brand character, berisi brand kartu yang digunakan dengan 3 jenis yaitu mastercard, visa, other
    card_type character, berisi tipe kartu debit, kredit, dan other
    card_number integer, berisi nomor kartu expires date, berisi tanggal berlakunya kartu yang digunakan
    cvv integer, berisi nomor cvv yang berada di kartu baik debit, maupun kartu kredit
    has_chip boolean, tanda apakah kartu yang digunakan sudah menggunakan chip atau tidak
    num_cards_issued integer, menandakan edisi atau penerbitan kartu yang digunakan
    credit_limit biginteger, limit yang dimiliki oleh kartu yang digunakan
    ```

2. users_data.csv (2000 record)

    merupakan data yang berisi informasi dari pengguna kartu sebagai pemilik kartu. Terdiri dari kolom:

    ```
    id : type biginteger, sebagai primary key 
    current_age integer, umur dari pengguna kartu
    retirement_age integer, umur pensiun dari pengguna kartu
    birth_year integer, tahun lahir dari pengguna
    birth_month integer, bulan lahir dari pengguna
    gender character, berisi gender dari pengguna kartu laki-laki dan perempuan
    address character, alamat dari pengguna kartu
    latitude float, titik koordinat latitude pengguna kartu
    longitude float, titik koordinat longitude pengguna kartu
    per_capita_income, pendapatan pengguna per kapita
    ```

3. transactions_data.csv (13.3 juta record)

    merupakan data yang berisi informasi transaksi kartu dengan merchant yang dilakukan oleh pengguna. Terdiri dari kolom:
    ```
    id : typebig integer, sebagai primary key
    date date: waktu pengguna melakukan transaksi
    client_id biginteger, sebagai foreign key yang terhubung dengan data users_data.csv
    card_id biginteger, sebagai foreign key yang terhubung dengan data cards_data.csv
    amount biginteger, jumlah transaksi yang dilakukan di merchant
    merchant_id biginteger, merchant tempat terjadinya transaksi
    merchant_city character, kota merchant yang terjadi transaksi
    merchant_state character, kode negara bagian yang berada di wilayah Amerika Serikat 
    zip float, berisi kode pos dari merchant
    ```


# ETL Pipeline Details
- Extract
    
    Extract data dilakukan terhadap beberapa sumber yang sudah dirancang sebelumnya, data akan diambil dari postgreSQL dan API yang kemudian disimpan di dalam minio dalam format parquet 
- Transform

    Transform data dilakukan menggunakan service spark dengan 2 klaster untuk handling file parquet yang sudah disimpan di minio. Setelah data di peroleh data diproses dengan membuat schema, melakukan formating beberapa tipe data, karena ada beberapa data yang tidak memiliki tipe data yang sesuai kemudian data disimpan ke postgresSQL sebagai data warehouse.

- Load

    Load data selain dilakukan di write setelah tranform data dengan spark, dilakukan load data lagi yang sudah berbentuk kimball model kedalam data warehouse menggunakan service DBT agar subjek bisa melakukan analisis di data mart.

# Step-by-Step Implementation
1. Masuk kedalam directory utama repository ini. Pastikan sudah berada di posisi `/analytic_financial_transaction` ketika menjalankan perintah `pwd`

2. Jalankan perintah `make create-network` untuk membuat docker network agar semua service saling terhubung

3. Tahap selanjutnya jalankan perintah `make docker-build` untuk membuat image docker baru sesuai project

4. Jalankan perintah `make docker-compose` untuk membuat docker container sesuai docker file untuk tiap service

```
Note:
untuk data yang digunakan untuk ingestion data diambil dari https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets kemudian data seperti cards_data.csv, transactions_data.csv, dan users_data.csv di insert kedalam postgreSQL secara manual
```

# Key Features
Staging area, Data warehouse, orchestration, visualization

# Performance Optimization
Strategi yang digunakan pada project ini adalah paralelisasi untuk beberapa task airflow flow terutama ketika melakukan ingestion data dari beberapa sumber, kemudian menggunakan spark cluster dengan 2 node untuk handling transoformasi data dalam jumlah besar

# Challenges and Solutions
Tantangan yang dihadapi pada pengembangan project ini adalah:
1. Mengembangkan API yang bisa diakses oleh airflow untuk ingestion data karena jumlah data yang banyak memerlukan waktu penarikan yang lama sehingga diperlukan filter agar data yang diambil bisa dibatasi
2. Tranformasi data dengan spark ketika mengambil data dari storage minIO dengan airflow. Pada tahap ini diperlukan penyesuaian versi spark yang ada di spark master, spark cluster, dan spark yang ada di airflow agar proses running task SparkSubmitOperator bisa berjalan. Selain itu diperlukan penyesuian versi hadoop dan amazon s3 yang bisa digunakan sesuai versi spark yang digunakan
3. Pengembangan data modeling dengan DBT, beberapa tantangan ketika melakukan data modeling adalah menjalankan DBT dengan menggunakan airflow, untuk solusi pada tahap ini dilakukan tahap secara manual


# Future Enhancements
Untuk pengembangan selanjutnya disarankan untuk menjalankan DBT secara otomatis dengan menggunakan API yang sama di FastAPI, sehingga nanti ketika di airflow hanya perlu melakukan hit ke API DBT nya.
