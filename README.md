# Introduction

Proyek ini bertujuan untuk merancang pipeline ETL (Extract, Transform, Load) untuk menganalisis perilaku pelanggan saat menggunakan kartu kredit. Tujuan proyek ini adalah agar tim marketing dapat memberikan diskon atau promo kepada pelanggan yang bertransaksi di merchant yang menjadi mitra layanan kartu kredit. Hasil dari proyek ini adalah data analisis yang memberikan ringkasan mengenai merchant dengan jumlah transaksi terbanyak di setiap kota.

# Project Overview
Jelaskan tujuan utama dari proyek ini, seperti mengotomatisasi alur data atau memproses data besar untuk analisis bisnis.

# Architecture Diagram
Sertakan diagram arsitektur ETL yang menggambarkan alur data mulai dari sumber hingga penyimpanan akhir. Gunakan alat seperti Lucidchart atau draw.io.

# Tools and Technologies Used
Daftar semua alat, framework, dan bahasa pemrograman yang digunakan (contoh: Apache Airflow, Spark, Python, Kafka, Minio, Hadoop).

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

Jelaskan proses pengambilan data dari sumbernya.
Contoh kode (jika ada).
- Transform

Jelaskan bagaimana data dibersihkan, diproses, atau diubah agar siap untuk dimuat.
Teknik yang digunakan (contoh: agregasi, normalisasi).
- Load

Jelaskan bagaimana data dimuat ke data warehouse atau data lake.
Solusi penyimpanan yang digunakan (contoh: Hadoop HDFS, BigQuery).

# Step-by-Step Implementation
- Environment Setup

Berikan instruksi untuk mengatur lingkungan proyek, termasuk instalasi dependencies.

- Code Workflow

Jelaskan alur kerja kode secara rinci.

- Pipeline Execution 

Jelaskan bagaimana pipeline dapat dijalankan (contoh: menggunakan Airflow DAGs atau script).

# Key Features
Highlight fitur-fitur unggulan dari pipeline Anda, seperti fault tolerance, skalabilitas, atau monitoring.

# Performance Optimization
Diskusikan strategi yang digunakan untuk meningkatkan kinerja, seperti paralelisasi, caching, atau indexing.

# Challenges and Solutions
Sebutkan tantangan yang dihadapi selama pengembangan proyek dan bagaimana Anda mengatasinya.

# How to Use
Berikan panduan langkah-langkah untuk menjalankan proyek ini, termasuk perintah terminal (jika ada).

# Future Enhancements
Bagikan rencana pengembangan di masa depan, seperti integrasi machine learning atau visualisasi data.

# References
Sebutkan referensi atau dokumentasi yang membantu Anda selama pengembangan proyek.

# Contact
Berikan detail kontak atau tautan ke profil LinkedIn/GitHub Anda jika seseorang ingin menghubungi Anda untuk pertanyaan atau kolaborasi.