# HYCANE: Riset Social Listening Hidroponik

Dokumen ini menjelaskan apa yang dilakukan dalam riset ini, bagaimana caranya, apa hasilnya, dan apa artinya bagi HYCANE. Bagian awal ditulis agar mudah dipahami siapa saja. Bagian teknis ada di belakang bagi yang ingin memeriksa atau mengulang prosesnya.

Riset dijalankan pada 7 sampai 8 Oktober 2026. Data dibekukan (tidak ditambah lagi) pada 7 Oktober 2026 pukul 21.32 UTC.

---

## Daftar Isi

1. [Ringkasan dalam 1 Menit](#1-ringkasan-dalam-1-menit)
2. [Kesimpulan Utama untuk Orang Awam](#2-kesimpulan-utama-untuk-orang-awam)
3. [Latar Belakang: Kenapa Riset Ini Dibuat](#3-latar-belakang-kenapa-riset-ini-dibuat)
4. [Pertanyaan yang Ingin Dijawab](#4-pertanyaan-yang-ingin-dijawab)
5. [Gambaran Besar Proses](#5-gambaran-besar-proses)
6. [Proses Langkah demi Langkah](#6-proses-langkah-demi-langkah)
7. [Hasil Lengkap](#7-hasil-lengkap)
8. [Uji Asumsi HYCANE](#8-uji-asumsi-hycane)
9. [Bukti yang Melemahkan Konsep HYCANE](#9-bukti-yang-melemahkan-konsep-hycane)
10. [Rekomendasi untuk HYCANE](#10-rekomendasi-untuk-hycane)
11. [Yang Belum Diketahui dan Harus Diuji Berikutnya](#11-yang-belum-diketahui-dan-harus-diuji-berikutnya)
12. [Keterbatasan Riset](#12-keterbatasan-riset)
13. [Cara Membaca Angka dalam Riset Ini](#13-cara-membaca-angka-dalam-riset-ini)
14. [Etika, Privasi, dan Aturan Akses](#14-etika-privasi-dan-aturan-akses)
15. [Struktur Folder dan File Penting](#15-struktur-folder-dan-file-penting)
16. [Cara Menjalankan Ulang](#16-cara-menjalankan-ulang)
17. [Glosarium](#17-glosarium)

---

## 1. Ringkasan dalam 1 Menit

Riset ini "mendengarkan" percakapan publik di internet tentang hidroponik untuk mengetahui apa yang benar-benar dialami, dikeluhkan, dan diinginkan orang. Hasilnya dipakai untuk menguji apakah ide HYCANE menjawab masalah nyata.

| Hal | Angka |
|---|---|
| Postingan dan komentar publik yang dikumpulkan (unik) | 136.019 |
| Lolos penyaringan (relevan, bukan spam, bukan duplikat) | 93.125 |
| Murni suara pelanggan (tanpa berita, promosi, dan konteks ganja) | 91.068 |
| Berbahasa Indonesia | 30.703 (33,7%) |
| Jumlah platform | 8 (YouTube, Reddit, forum GardenWeb, Mastodon, Hacker News, Bluesky, Lemmy, Stack Exchange) |
| Rentang waktu percakapan | 2002 sampai Oktober 2026 |
| Publikasi ilmiah yang dikumpulkan | 677 (14 dibaca dan dirangkum khusus) |
| Sumber pakar atau lembaga | 7 |

Inti temuannya:

- **Masalah terbesar orang yang menanam hidroponik adalah tanaman yang rusak atau mati.** Penyebabnya antara lain akar busuk, daun menguning, layu, hama, nutrisi yang salah takar, dan pH yang tidak stabil.
- **Yang paling banyak diminta orang adalah tutorial, komunitas, dan cara memantau pH serta kepekatan nutrisi (TDS/EC).**
- **Ampas tebu dan isu ramah lingkungan hampir tidak dibicarakan pengguna** sebagai alasan memilih atau membeli produk.
- **Banyak orang sangat hemat dan suka membuat sistem sendiri (DIY).** Ini tantangan besar untuk kit seharga Rp910.000.

---

## 2. Kesimpulan Utama untuk Orang Awam

Bagian ini menjelaskan hasil riset dengan bahasa sehari-hari.

### Kesimpulan 1: Orang tidak butuh "teknologi canggih", orang butuh tanamannya tidak mati

Keluhan nomor satu, di semua platform, adalah tanaman yang sakit atau mati. Orang bertanya "kenapa daun saya menguning?", "kenapa akarnya busuk?", "kenapa kangkung saya layu terus?".

Ibaratnya seperti memelihara ikan di akuarium. Masalahnya sering tidak terlihat (kualitas air), dan baru ketahuan setelah ikannya sakit. Hidroponik sama: pH, kepekatan nutrisi, dan suhu air tidak terlihat mata, tetapi menentukan hidup matinya tanaman.

**Artinya bagi HYCANE:** fitur sensor dan aplikasi memang relevan, tetapi yang dijual seharusnya hasilnya ("tanaman Anda tidak mati"), bukan teknologinya ("sistem IoT berbasis AI").

### Kesimpulan 2: Pemula adalah kelompok paling besar dan paling butuh bantuan

Dari orang yang menyebutkan pengalamannya, sekitar 84% adalah pemula atau orang yang belum pernah mencoba. Di YouTube Indonesia, komentar paling banyak berupa ucapan terima kasih atas tutorial dan pertanyaan langsung ke pembuat video, misalnya "Kak, ini pakai pipa ukuran berapa?" atau "AB mix-nya berapa ml?".

**Artinya bagi HYCANE:** sasaran utama yang paling jelas adalah pemula. Mereka butuh dipandu langkah demi langkah.

### Kesimpulan 3: Edukasi dan komunitas adalah "pintu masuk" pelanggan

Permintaan eksplisit paling banyak adalah tutorial atau edukasi (228 permintaan, muncul di 8 platform), lalu komunitas (62 permintaan, 7 platform). Orang Indonesia belajar hidroponik terutama dari kreator YouTube.

**Artinya bagi HYCANE:** bekerja sama dengan kreator YouTube hidroponik dan mengadakan workshop kemungkinan lebih efektif daripada iklan biasa.

### Kesimpulan 4: Ampas tebu bukan alasan orang membeli

Dari 91.068 komentar pelanggan, ampas tebu sebagai media tanam hanya disebut 18 kali. Ketika orang membicarakan ampas tebu (bagasse) di internet, biasanya konteksnya piring sekali pakai, kemasan, atau bahan bakar, bukan media tanam. Yang sering dikeluhkan justru rockwool, misalnya bikin gatal, mengganggu pH, dan sulit dibuang (sekitar 160 rekaman).

**Artinya bagi HYCANE:** ampas tebu tetap bisa menjadi keunggulan, tetapi harus dijual sebagai media yang **praktis dan tidak merepotkan**, bukan sekadar "ramah lingkungan". Kinerjanya juga harus dibuktikan dulu di laboratorium karena belum ada penelitian ilmiah yang menguji ampas tebu sebagai media hidroponik air.

### Kesimpulan 5: Ramah lingkungan itu "bonus", bukan alasan utama membeli

Bahasa positif tentang keberlanjutan hanya muncul di 0,65% percakapan. Pada percakapan yang menunjukkan niat membeli, isu lingkungan muncul di sekitar 11%, sedangkan harga dan biaya muncul di sekitar 33%. Kritik yang ada justru soal listrik ("boros listrik ya pakai pompa?").

**Artinya bagi HYCANE:** keberlanjutan tetap penting untuk tema kompetisi RISE, tetapi sebaiknya menjadi nilai pendukung, bukan pesan utama penjualan.

### Kesimpulan 6: Pesaing terbesar HYCANE adalah "bikin sendiri"

Bahasa hemat atau murah (2.256 rekaman) jauh lebih banyak daripada bahasa premium (455 rekaman), sekitar 5 banding 1. Komentar seperti "saya bisa bikin ini jauh lebih murah" muncul di 7 platform. Ada juga kelompok yang lebih suka sistem pasif tanpa listrik seperti Kratky atau sistem sumbu (189 rekaman, 8 platform).

**Artinya bagi HYCANE:** harga harus dijelaskan dengan membandingkan total biaya membuat sendiri ditambah kerugian kalau gagal panen. Sebaiknya ada versi murah atau versi awal.

### Kesimpulan 7: Hati-hati dengan model langganan dan ketergantungan aplikasi

Pemilik smart garden mengeluhkan harga pod benih sekitar 5 dolar per buah, aplikasi yang tidak mengirim notifikasi, dan WiFi yang sering putus. AeroGarden, merek smart garden paling terkenal, sempat diumumkan akan ditutup pada akhir 2024 sebelum kembali pada 2025.

**Artinya bagi HYCANE:** kit harus tetap bisa dipakai tanpa langganan dan tanpa aplikasi. Isi ulang media dan nutrisi sebaiknya terbuka, tidak "dikunci" ke merek sendiri.

### Kesimpulan 8: Beberapa asumsi lama belum bisa dibuktikan

Usia 20 sampai 40 tahun, penerimaan harga Rp910.000, dan prioritas Pulau Jawa **tidak bisa dibuktikan** dari percakapan publik. Orang jarang menyebutkan usia atau lokasi. Semua ini harus diuji lewat survei atau uji coba langsung.

### Satu kalimat penutup

> Masalah yang dijawab HYCANE itu nyata (tanaman pemula sering mati karena kondisi air tidak terpantau), tetapi cara menjualnya perlu diubah: fokus pada "panen berhasil dan dipandu", bukan pada "AI, IoT, dan ampas tebu".

---

## 3. Latar Belakang: Kenapa Riset Ini Dibuat

HYCANE adalah konsep ekosistem hidroponik pintar yang dikembangkan untuk **BPC RISE 2026** dengan tema "From Vision to Venture: Membangun Bisnis yang Inovatif dan Berkelanjutan" dan subtema "Agroteknologi & Ketahanan Pangan". HYCANE menggabungkan:

- media tanam dari ampas tebu yang dirancang mudah terurai (biodegradable);
- sistem hidroponik;
- sensor IoT untuk pH, TDS/EC, suhu, dan ketinggian air;
- penyimpanan data dan analisis berbasis AI;
- aplikasi mobile untuk pemantauan, peringatan, dan panduan;
- edukasi, komunitas, dan produk isi ulang (media, nutrisi, suku cadang);
- peluang B2B dan institusi.

Dosen pembimbing meminta bukti yang lebih kuat dari percakapan nyata di internet tentang:

- apakah orang benar-benar tertarik dengan hidroponik;
- apa yang membuat mereka kesulitan atau berhenti;
- fitur apa yang mereka inginkan;
- seperti apa persona pelanggan yang bisa dipertanggungjawabkan.

Saat riset dimulai, semua klaim pelanggan dalam dokumen HYCANE masih berupa **asumsi**: target usia 20 sampai 40 tahun, kalangan menengah, prioritas Jawa, peduli lingkungan, tertarik smart farming, serta harga kit Rp910.000. Dokumen tim sendiri menyebutkan bahwa prototipe masih tahap rancangan dan survei pasar primer belum dilakukan. Detailnya ada di `outputs/source_inventory.md`.

---

## 4. Pertanyaan yang Ingin Dijawab

Riset ini menjawab 27 pertanyaan riset (RQ01 sampai RQ27). Kelompok besarnya:

1. **Bagaimana hidroponik dibicarakan?** Topik, nada (sentimen), dan perbedaan antar platform.
2. **Apa keluhan yang paling sering dan paling berat?** Termasuk perbedaan pemula dan yang berpengalaman, serta Indonesia dan global.
3. **Apa niat orang saat berbicara?** Mencari info, memecahkan masalah, membandingkan, ingin membeli, atau menyerah.
4. **Fitur apa yang diminta secara langsung dan apa yang hanya tersirat dari keluhan?**
5. **Seberapa penting harga, kemudahan, ruang sempit, otomatisasi, sensor, AI, edukasi, dan keberlanjutan?**
6. **Apakah ampas tebu dianggap bernilai oleh pelanggan?**
7. **Persona apa yang muncul dari data, tanpa memaksakan demografi?**
8. **Apakah asumsi segmentasi HYCANE didukung data?**
9. **Bukti apa yang justru melemahkan konsep HYCANE?**
10. **Apa yang harus diubah di proposal, dan apa yang masih harus diuji langsung?**

---

## 5. Gambaran Besar Proses

Alurnya seperti ini:

```
Membaca dokumen HYCANE dan aturan riset
        |
Audit komputer, kunci API, dan izin akses tiap platform
        |
Mengumpulkan data publik (API resmi dan halaman publik yang diizinkan)
        |
RAW     : simpan data mentah apa adanya (tidak pernah diubah)
        |
BRONZE  : ubah semua platform ke format kolom yang sama
        |
SILVER  : bersihkan teks, deteksi bahasa, nilai relevansi, saring spam, buang duplikat
        |
GOLD    : data final siap analisis + label sentimen, topik, keluhan, niat, fitur, persona
        |
INSIGHT : tabel, grafik, dashboard, uji asumsi, kontradiksi, rekomendasi, laporan
```

Di samping data percakapan, ada dua aliran bukti yang **dipisahkan**:

- **Bukti akademik:** jurnal ilmiah dari OpenAlex dan Crossref.
- **Bukti pakar:** panduan penyuluhan universitas dan liputan media kredibel.

Ketiganya dibandingkan di akhir (triangulasi), tetapi tidak pernah dicampur dalam satu hitungan.

---

## 6. Proses Langkah demi Langkah

### 6.1 Membaca dokumen dan inventaris sumber

Semua file spesifikasi riset (23 file Markdown) dibaca. Dokumen HYCANE dan RISE yang ditemukan di folder Downloads dan Documents juga dibaca, antara lain:

- Guidebook BPC RISE 2026;
- Checklist RISE;
- BMC HYCANE;
- proposal LUMINUX, FESTAFORA, dan AGTION;
- makalah CaneBioKit.

Setiap dokumen dicatat relevansinya dan dibedakan antara fakta dan asumsi.

Hasil: `outputs/source_inventory.md`.

### 6.2 Audit lingkungan dan akses sumber

Pemeriksaan meliputi versi Python, paket yang terpasang, koneksi internet, ruang penyimpanan, kunci API, dan status Git. Setiap platform kemudian diuji: bisa diakses atau tidak, perlu kunci atau tidak, berapa batas kuotanya, dan apa alternatifnya bila diblokir.

Awalnya tidak ada satu pun kunci API. Di tengah proses, tim menambahkan **kunci YouTube Data API**, sehingga data berbahasa Indonesia melonjak dari sekitar 83 rekaman menjadi lebih dari 30 ribu.

Hasil: `outputs/environment_audit.md` dan `outputs/source_access_audit.md`.

Status akses tiap sumber:

| Sumber | Status | Keterangan |
|---|---|---|
| YouTube | Berhasil | API resmi; 1.061 video, 83.303 komentar; 7.445 dari 10.000 unit kuota harian terpakai |
| Reddit | Berhasil lewat arsip | API resmi butuh kredensial yang tidak dimiliki; memakai arsip riset publik Arctic Shift |
| Forum GardenWeb (Houzz) | Berhasil | Halaman publik; setiap alamat dicek dulu ke robots.txt |
| Mastodon, Lemmy, Bluesky | Berhasil | API publik |
| Hacker News, Stack Exchange | Berhasil | API resmi |
| X (Twitter), TikTok, Instagram, Facebook, Threads | Tidak tersedia | Butuh kredensial atau izin riset yang tidak dimiliki |
| Kaskus | Diblokir | Fitur pencariannya memakai jalur `/api/` yang dilarang robots.txt |
| Kompasiana | Diblokir | Ketentuan situs melarang penambangan teks |
| Quora | Diblokir | Menolak akses (kode 403) |
| Tokopedia, Shopee, Amazon | Tidak tersedia | Tidak ada akses ulasan publik yang diizinkan |
| OpenAlex, Crossref | Berhasil | Untuk jurnal ilmiah |
| Semantic Scholar | Dibatasi | Kena batas kuota tanpa kunci |

### 6.3 Menyusun daftar kata kunci pencarian

Kata kunci disusun dalam 14 kelompok, dalam bahasa Indonesia dan Inggris. Contohnya:

| Kelompok | Contoh kata kunci |
|---|---|
| Inti | hidroponik, hydroponics |
| Pemula | hidroponik pemula, belajar hidroponik |
| Kegagalan | hidroponik gagal, daun kuning hidroponik, akar busuk |
| Nutrisi | pH hidroponik, TDS, EC, ppm, AB mix |
| Air dan lingkungan | suhu air hidroponik, aerator |
| IoT | sensor hidroponik, hidroponik otomatis, smart hydroponic |
| AI | AI hidroponik |
| Pembelian | harga kit hidroponik, rekomendasi kit |
| Keberlanjutan | media tanam ramah lingkungan, biodegradable |
| Ampas tebu | ampas tebu media tanam, bagasse |
| Lahan sempit | hidroponik balkon, lahan sempit |
| Pengalaman | kesalahan hidroponik pemula |
| Produk | AeroGarden, Click & Grow, Gardyn, Kratky |

Setiap kata kunci punya kode unik. Dengan begitu, setiap rekaman bisa dilacak ke kata kunci yang menemukannya.

Hasil: `config/queries.yaml`.

### 6.4 Mengumpulkan data

Setiap platform punya "pengumpul" (collector) sendiri:

- **YouTube:** mencari video dengan kata kunci Indonesia sebagai prioritas, lalu mengambil komentar dan balasannya. Komentar dibatasi 300 utas per video supaya satu video viral tidak mendominasi.
- **Reddit:** mengambil sampel postingan per kuartal dari komunitas hidroponik (r/Hydroponics, r/hydro, r/kratky, r/aerogarden, dan lainnya), pencarian kata kunci di komunitas umum dan Asia Tenggara (r/indonesia, r/malaysia, r/singapore, r/Philippines), lalu 300 utas komentar yang dipilih merata per komunitas dan tahun.
- **Forum GardenWeb:** daftar diskusi hidroponik, lalu 1.626 utas diambil secara acak terkendali.
- **Platform lain:** pencarian kata kunci atau tagar.

Prinsip teknis yang dipakai:

- **Sopan:** ada jeda antar permintaan supaya tidak membebani server.
- **Coba ulang otomatis** bila server sibuk.
- **Checkpoint:** kalau proses terhenti, bisa dilanjutkan dari titik terakhir.
- **Buku catatan permintaan:** semua permintaan (5.142 permintaan) dicatat lengkap, termasuk waktu dan hasilnya, tanpa pernah mencatat kunci rahasia.
- **Isolasi kegagalan:** kalau satu sumber gagal, sumber lain tetap jalan.

### 6.5 Lapisan data: RAW, BRONZE, SILVER, GOLD

- **RAW:** setiap respons dari platform disimpan utuh dalam file terkompresi dan **tidak pernah diubah**. Ini "bukti asli".
- **BRONZE:** data dari 8 platform yang formatnya berbeda-beda disatukan ke format kolom yang sama: siapa (dalam bentuk kode acak), kapan, di mana, teks, dan tautan sumber. Ada 150.708 baris karena satu postingan bisa ditemukan oleh beberapa kata kunci.
- **SILVER:** setiap objek dihitung sekali, menjadi 136.019 objek unik, lalu dibersihkan dan diberi tanda (lihat 6.6).
- **GOLD:** data yang lolos semua saringan, sebanyak 93.125 rekaman, lengkap dengan label analisis.

Setiap rekaman GOLD punya jejak ke file mentahnya dan kode sidik jari (provenance hash), sehingga bisa diperiksa ulang kapan saja.

### 6.6 Membersihkan dan menyaring data

| Langkah | Apa yang dilakukan | Hasil |
|---|---|---|
| Membersihkan teks | Menghapus kode HTML, merapikan spasi, menyeragamkan karakter. Teks asli tetap disimpan terpisah | Teks rapi untuk analisis |
| Mengambil elemen khusus | Tautan, mention (@), tagar (#), dan jumlah emoji | Kolom terpisah |
| Deteksi bahasa | Alat deteksi untuk 29 bahasa. Teks yang terdeteksi Melayu dari pencarian berbahasa Indonesia dikoreksi menjadi Indonesia karena alat sering tertukar | Kolom bahasa dan tingkat keyakinan |
| Skor relevansi | Apakah teks benar-benar tentang hidroponik (kata kunci kuat, komunitas khusus hidroponik, atau judul utas) | 22,9% objek tidak relevan dan dibuang |
| Makna yang tidak berkaitan | Contoh: "hydro" yang berarti listrik tenaga air, ampas tebu untuk piring sekali pakai, Rockwool sebagai perusahaan insulasi, game, nama orang | 443 rekaman dikeluarkan |
| Konteks ganja | Banyak diskusi hidroponik berbahasa Inggris membahas ganja, yang di luar pasar HYCANE dan ilegal di Indonesia. Ditandai dan dikeluarkan dari analisis inti | 1,5% dari gold |
| Berita dan promosi | Siaran pers, iklan, dan pengumuman lembaga dipisahkan dari suara pelanggan | 0,7% dari data inti |
| Spam | Kode alasan yang transparan: promosi, banyak tautan, hanya tautan, teks berulang dari akun yang sama, promosi channel. Komentar negatif **tidak** dianggap spam | 0,31% dari data relevan |
| Duplikat | Enam lapis: ID sama, teks persis sama, teks sama setelah dinormalisasi, tautan dan teks sama, teks hampir sama (MinHash), makna hampir sama (kemiripan embedding di atas 0,95) | 2,9% duplikat teks dan 348 duplikat makna dibuang |

### 6.7 Analisis sentimen (nada positif atau negatif)

Setiap teks diberi label POSITIF, NETRAL, NEGATIF, CAMPURAN (MIXED), atau AMBIGU.

Ada empat kandidat model yang dibandingkan:

1. **Kamus kata** (VADER untuk bahasa Inggris dan kamus buatan sendiri untuk bahasa Indonesia, termasuk penanganan kata negasi seperti "tidak", "gak", "belum").
2. **XLM-RoBERTa multibahasa** (model AI yang dilatih dari tweet berbagai bahasa).
3. **XLM-R dengan IndoRoBERTa khusus untuk teks Indonesia.**
4. **Model zero-shot**, yang hanya diuji coba lalu tidak dipakai karena salah membaca sarkasme dan kalimat seperti "bagus sih tapi ribet".

**Cara memilih model:** 420 rekaman diambil secara terstratifikasi (merata per platform, bahasa, dan label), termasuk kasus sulit:

- slang Indonesia;
- negasi;
- campur bahasa;
- emoji;
- singkatan teknis;
- sarkasme.

Rekaman ini diberi label pembanding, lalu tiap model dinilai.

| Model | Akurasi 3 kelas | Macro F1 3 kelas |
|---|---|---|
| **XLM-R (dipilih)** | **0,72** | **0,66** |
| XLM-R dengan IndoRoBERTa | 0,61 | 0,58 |
| Kamus kata | 0,57 | 0,48 |

Akurasi XLM-R pada teks Indonesia adalah 0,84. Rincian per kasus sulit:

| Kasus | Akurasi |
|---|---|
| Slang Indonesia | 0,83 |
| Negasi Indonesia | 0,78 |
| Emoji | 0,78 |
| Campur bahasa | 0,76 |
| Singkatan teknis | 0,71 |
| Negasi bahasa Inggris | 0,66 |
| Sarkasme | 0,64 |

**Catatan jujur:** label pembanding dibuat oleh AI (LLM) yang membaca setiap rekaman, **bukan oleh manusia**. Daftar untuk dilabeli manusia sudah disiapkan di `data/annotation/annotation_queue_human.csv`.

Selain sentimen keseluruhan, ada **sentimen per aspek**: nada kalimat yang menyebut 20 aspek seperti harga, pH, sensor, aplikasi, media tanam, dan keberlanjutan.

### 6.8 Menemukan topik pembicaraan

Komputer mengelompokkan teks yang maknanya mirip tanpa diberi tahu topiknya. Caranya:

1. Setiap teks diubah menjadi "sidik jari makna" (embedding) dengan model multibahasa MiniLM.
2. Dimensinya diringkas dengan UMAP.
3. Teks dikelompokkan dengan KMeans dan BERTopic.

Jumlah topik dipilih otomatis lewat skor kualitas (silhouette), dan hasilnya 35 topik. Metode alternatif (NMF dan HDBSCAN) juga dijalankan sebagai pembanding. Setiap topik kemudian **diberi nama oleh peneliti** setelah membaca kata kunci dan contoh teksnya.

### 6.9 Keluhan, niat, fitur, harga, dan keberlanjutan

Bagian ini memakai **taksonomi berbasis aturan** yang transparan (daftar pola kata dalam bahasa Indonesia dan Inggris) di file `config/taxonomy.yaml`.

- **Keluhan (pain points):** 21 kategori, misalnya kesehatan tanaman, nutrisi, pH, EC/TDS, suhu, oksigen, peralatan, biaya, pengetahuan, sensor, aplikasi, dan media tanam. Sebuah kalimat dihitung sebagai keluhan bila menyebut topik **dan** tanda masalah (misalnya "pH-nya naik terus", "daunnya menguning", "kok gak tumbuh").
- **Tingkat keparahan:** skor dasar per kategori, ditambah bila ada kata kehilangan besar ("semua mati", "gagal terus").
- **Prioritas keluhan:** Frekuensi × Keparahan × Keberulangan (muncul di banyak bulan) × Keluasan (muncul di banyak platform) × Relevansi bagi HYCANE. Ada tiga skema bobot untuk menguji apakah urutannya berubah.
- **Niat (intent):** 11 kelas, yaitu kesadaran, inspirasi, mencari info, memecahkan masalah, membandingkan, menjajaki pembelian, niat beli eksplisit, setelah membeli, merekomendasikan, frustrasi atau menyerah, dan tidak diketahui. **Niat membeli tidak pernah disimpulkan dari nada positif.**
- **Fitur:** dibedakan antara **disebut** dan **diminta secara eksplisit** ("seandainya ada...", "I wish...", "butuh..."). Ada juga **permintaan tersirat** dari keluhan, misalnya keluhan pH yang menyiratkan kebutuhan pemantauan pH.
- **Harga:** pertanyaan harga, keberatan harga, bahasa murah atau premium, langganan, dan angka harga.
- **Keberlanjutan:** positif, netral, skeptis, atau negatif.
- **Kontradiksi:** pola yang membantah asumsi HYCANE, seperti tidak perlu otomatisasi, tidak percaya sensor, tidak suka aplikasi atau langganan, lebih murah bikin sendiri, kembali ke tanah, dan skeptis keberlanjutan.

**Pengujian aturan:** aturan versi pertama ternyata lemah. Presisi deteksi keluhannya hanya 0,16, artinya banyak salah tangkap. Aturan diperbaiki **satu kali** dengan hanya melihat separuh sampel validasi (210 rekaman). Hasilnya diuji pada separuh lainnya yang tidak pernah dilihat:

| Aturan | Sebelum perbaikan | Sesudah perbaikan (data uji) |
|---|---|---|
| Keluhan: presisi per kategori | 0,16 | 0,27 |
| Keluhan: recall per kategori | 0,25 | 0,31 |
| Keluhan: presisi "ada keluhan atau tidak" | | 0,48 |
| Niat: akurasi | 0,37 | 0,45 |
| Niat: macro F1 | 0,21 | 0,29 |
| Tingkat pengalaman: akurasi | 0,82 | |
| Relevansi data gold | 93% benar-benar relevan | |

**Artinya:** jumlah absolut keluhan dan niat adalah perkiraan kasar. Yang dapat diandalkan adalah **urutan**, karena urutannya terbukti stabil di semua uji.

### 6.10 Persona

Persona dibentuk dari **pola percakapan**, bukan dari demografi. Satu orang biasanya hanya berkomentar sekali, sehingga yang dikelompokkan adalah jenis percakapannya.

- Data yang dipakai: 31.114 rekaman suara pelanggan yang punya minimal 2 ciri informatif. Cirinya ada 46, meliputi tingkat pengalaman, niat, keluhan, fitur, sinyal harga, keberlanjutan, merek kit, konteks ruang sempit, aspek teknologi, dan kontradiksi.
- Metode: dicoba 2 sampai 8 kelompok (KMeans), lalu dipilih berdasarkan kualitas pemisahan, kestabilan bila data diacak ulang, kecocokan dengan metode lain (Ward), dan ukuran kelompok terkecil. **Terpilih 4 persona.**
- Uji ketahanan: dihitung ulang dengan jumlah data per platform yang disamakan, dan dengan tanpa YouTube.
- Usia, jenis kelamin, pendapatan, dan sifat sensitif lain **tidak pernah ditebak**.

### 6.11 Bukti akademik dan pakar

- **Akademik:** 677 publikasi dari OpenAlex dalam 9 bidang, yaitu hambatan adopsi, pengetahuan pemula, nutrisi/pH/EC, IoT, AI, media tanam dan ampas tebu, keberlanjutan, penerimaan konsumen, dan konteks Indonesia. Sebanyak 48 DOI dicek silang ke Crossref, dan 14 publikasi paling relevan dibaca abstraknya serta dirangkum.
- **Pakar:** 7 sumber dibaca lengkap: penyuluhan Colorado State University, University of Kentucky, University of Illinois, University of Missouri/SARE, UF/IFAS, serta liputan Texas Standard dan Bob Vila tentang penutupan dan kembalinya AeroGarden. Ada 3 sumber yang tidak bisa dibaca, jadi tidak dipakai.
- **Triangulasi:** setiap temuan dicek apakah suara pelanggan, akademik, dan pakar sepakat, bertentangan, atau hanya salah satu yang ada.

### 6.12 Visualisasi dan dashboard

Ada 20 grafik dalam format PNG dan SVG. Setiap grafik mencantumkan jumlah data (n), penyebut persentase, rentang waktu, lapisan data, dan apa saja yang dikeluarkan.

Dashboard interaktif menyediakan filter platform, sumber, bahasa, negara, pengalaman, niat, sentimen, topik, persona, dan tanggal.

### 6.13 Pemeriksaan kualitas (QA)

Ada 42 tes otomatis, dan semuanya **lulus**. Tes ini memeriksa:

- tidak ada ID ganda;
- setiap rekaman punya sumber dan file mentahnya ada;
- sampel acak 150 rekaman benar-benar bisa dilacak ke file mentah;
- tidak ada nama akun asli yang tersimpan;
- tidak ada kunci rahasia di log;
- data akademik tidak tercampur dengan data pelanggan;
- semua grafik, tabel, dan dashboard ada;
- angka di laporan cocok dengan data.

---

## 7. Hasil Lengkap

Semua angka berasal dari file di `outputs/tables/`. Persentase memakai **91.068 rekaman suara pelanggan** sebagai penyebut, kecuali disebutkan lain.

### 7.1 Sebaran data per platform

| Platform | Objek unik | Gold | Suara pelanggan | Persen bahasa Indonesia | Rentang tahun |
|---|---|---|---|---|---|
| YouTube | 83.303 | 55.271 | 54.622 | 56,0% | 2013 sampai 2026 |
| Reddit | 22.402 | 19.625 | 18.931 | 0,3% | 2009 sampai 2026 |
| Forum GardenWeb | 10.904 | 10.778 | 10.548 | 0% | 2002 sampai 2025 |
| Mastodon | 2.953 | 2.286 | 2.212 | 0,2% | 2017 sampai 2026 |
| Hacker News | 8.868 | 1.850 | 1.678 | 0% | 2008 sampai 2026 |
| Bluesky | 3.238 | 1.689 | 1.608 | 6,0% | 2014 sampai 2026 |
| Lemmy | 3.358 | 1.218 | 1.075 | 0% | 2020 sampai 2026 |
| Stack Exchange | 993 | 408 | 394 | 0% | 2011 sampai 2026 |
| **Total** | **136.019** | **93.125** | **91.068** | **33,7%** | **2002 sampai 2026** |

YouTube menyumbang sekitar 60% suara pelanggan. Karena itu, semua hasil penting juga dihitung ulang **tanpa YouTube**. Hasilnya tetap konsisten.

Bahasa pada data gold: Inggris 57.801, Indonesia 31.139, Tagalog 1.733, sisanya Jerman, Portugis, Spanyol, Melayu, dan lain-lain.

### 7.2 Nada percakapan (sentimen)

| Sentimen | Persen |
|---|---|
| Netral | 35,4% |
| Positif | 25,4% |
| Ambigu | 17,3% |
| Negatif | 16,0% |
| Campuran | 5,9% |

- **Percakapan berbahasa Indonesia lebih positif** (28,4% positif dan 11,0% negatif) dibanding bahasa Inggris (23,4% positif dan 19,1% negatif). Ini karena banyak komentar terima kasih atas tutorial.
- **Perbedaan antar platform nyata tetapi kecil sampai sedang** (Cramér's V 0,15). Forum tanya jawab seperti Stack Exchange, GardenWeb, dan Hacker News paling sedikit positifnya. YouTube dan Bluesky paling positif.
- **Topik paling negatif:**

  | Topik | Negatif |
  |---|---|
  | Hama | 45% |
  | Herba atau kemangi dan sistem pod | 34% |
  | Lumut dan oksigen | 29% |
  | Debat vertical farming | 27% |
  | Tomat dan cabai | 25% |
  | Kesehatan akar | 23% |

- **Aspek paling negatif:**

  | Aspek | Negatif |
  |---|---|
  | Kesehatan tanaman | 39% |
  | Kemudahan penggunaan | 28% |
  | Keberlanjutan | 26% |
  | Harga | 24% |
  | Suhu | 24% |

- **Sensor dan AI:** sensor lebih sering dibicarakan negatif (12%) daripada positif (6%). AI terbelah, 22% positif dan 23% negatif.

### 7.3 Topik pembicaraan (35 topik)

Topik-topik ini bisa dikelompokkan menjadi empat kelompok besar:

1. **Belajar dan apresiasi (YouTube Indonesia):**
   - balasan dan pertanyaan langsung ke kreator, 5.580 rekaman;
   - ucapan terima kasih atas tutorial, 5.250 (93% positif);
   - niat belajar, 3.419;
   - komentar tentang videonya, 2.075.
2. **Urusan kimia air:**
   - mencampur nutrisi dan ppm, 4.453;
   - AB mix, pupuk, dan rockwool, 3.080;
   - sumber dan penggantian air, 3.037;
   - alat ukur TDS/PPM dan kalibrasi, 2.257.
3. **Perangkat dan rakitan sendiri:**
   - pompa, pipa PVC, dan listrik, 1.902;
   - tandon, ember, dan DWC, 1.772;
   - keamanan plastik dan wadah bekas, 1.715;
   - ukuran pipa dan jarak lubang NFT, 1.655;
   - proyek rakitan, 1.186.
4. **Kegagalan:**
   - kesehatan akar, 3.105;
   - panas, hujan, dan suhu air (khas iklim tropis Indonesia), 1.702;
   - hama, 1.123;
   - lumut dan oksigen, 920.

Ada pula topik khusus **membeli: harga, beli di mana, dan modal** (2.733 rekaman).

Uji kejenuhan menunjukkan kombinasi topik dan keluhan baru per 100 rekaman turun dari 16,8 di awal menjadi 0 di akhir. Artinya, menambah data lagi kemungkinan besar tidak memunculkan tema baru.

### 7.4 Keluhan utama (pain points)

Urutan berdasarkan skor prioritas:

| Peringkat | Keluhan | Jumlah rekaman | Persen | Muncul di platform | Porsi bernada negatif | Rekaman Indonesia |
|---|---|---|---|---|---|---|
| 1 | Kesehatan tanaman | 4.754 | 5,2% | 8 | 0,37 | 967 |
| 2 | Nutrisi | 1.393 | 1,5% | 8 | 0,34 | 248 |
| 3 | pH | 687 | 0,8% | 8 | 0,32 | 106 |
| 4 | Peralatan rusak | 977 | 1,1% | 8 | 0,41 | 175 |
| 5 | Pengetahuan atau bingung | 1.688 | 1,9% | 8 | 0,35 | 151 |
| 6 | Suhu air | 459 | 0,5% | 8 | 0,38 | 106 |
| 7 | EC/TDS (kepekatan) | 439 | 0,5% | 7 | 0,33 | 164 |
| 8 | Biaya | 1.925 | 2,1% | 8 | 0,31 | 385 |

**Seberapa stabil urutannya?**

- Korelasi peringkat antar skema bobot adalah 0,99 dan 0,987, jadi hampir identik.
- Lima besar berdasarkan frekuensi selalu sama (kesehatan tanaman, biaya, pengetahuan, nutrisi, peralatan) pada delapan uji berbeda:
  - semua data;
  - hanya sentimen berkeyakinan tinggi;
  - termasuk konteks ganja;
  - termasuk berita dan promosi;
  - tanpa YouTube;
  - hanya komentar;
  - hanya postingan;
  - bobot per utas.
- Korelasi peringkat terendah adalah 0,96.

**Pemula dan yang berpengalaman.** Keluhan pengetahuan sama besarnya di kedua kelompok (4,2% dan 4,0%). Yang berpengalaman justru lebih banyak mengeluhkan biaya (7,1% berbanding 2,2%), kesehatan tanaman, peralatan, dan otomatisasi.

**Indonesia dan global.**

- Keluhan EC/TDS (ppm, kepekatan AB mix) relatif **lebih sering** di percakapan Indonesia (0,53% berbanding 0,46%).
- Keluhan lain lebih jarang di percakapan Indonesia karena banyak komentar berupa ucapan terima kasih.
- Di dashboard dengan filter bahasa Indonesia, EC/TDS naik ke peringkat 5 keluhan terbanyak.

**Ruang sempit hampir tidak pernah dikeluhkan** (9 rekaman). Ruang sempit adalah konteks, bukan masalah.

### 7.5 Niat percakapan dan sinyal pembelian

| Niat utama | Persen |
|---|---|
| Tidak diketahui | 35,5% |
| Mencari informasi | 25,5% |
| Inspirasi | 13,9% |
| Kesadaran (berita, opini umum) | 8,1% |
| Memecahkan masalah | 6,7% |
| Merekomendasikan | 5,9% |
| Membandingkan | 1,9% |
| Menjajaki pembelian | 1,0% (931 rekaman) |
| Setelah membeli | 0,7% (662) |
| Niat beli eksplisit | 0,45% (407) |
| Frustrasi atau menyerah | 0,34% (314) |

- **Niat berbeda antar platform** (Cramér's V 0,22). YouTube didominasi inspirasi dan pencarian info. Reddit, GardenWeb, dan Stack Exchange didominasi pemecahan masalah dan rekomendasi. Hacker News, Mastodon, dan Bluesky didominasi kesadaran dan debat.
- **Sinyal beli** kuat ada 330 rekaman dan sedang 483, total 0,9%. Hampir semuanya (779 dari sekitar 810 di data persona) berasal dari persona "Evaluator Hemat/DIY".
- **Dalam bahasa Indonesia**, sinyal beli berbentuk "beli di mana", "harga berapa", dan pembahasan modal.

### 7.6 Permintaan fitur

| Fitur | Disebut | Diminta eksplisit (jumlah platform) | Kelas bukti |
|---|---|---|---|
| Edukasi atau tutorial | 7.226 | 228 (8) | Diminta eksplisit |
| Komunitas | 1.171 | 62 (7) | Diminta eksplisit |
| Pemantauan TDS/EC | 763 | 46 (6) | Diminta eksplisit |
| Pemantauan pH | 615 | 31 (6) | Diminta eksplisit |
| Riwayat atau catatan data | 657 | 30 (5) | Diminta eksplisit |
| Diagnosis masalah | 311 | 18 (5) | Diminta eksplisit |
| Dashboard | 360 | 18 (5) | Diminta eksplisit |
| Mode pemula | 207 | 8 (2) | Tersirat kuat |
| Media mudah terurai | 73 | 8 (4) | Tersirat kuat, tetapi tidak menonjol |
| Pemantauan ketinggian air dan suhu | 149 dan 53 | 6 dan 5 | Tersirat kuat |
| Peringatan dan pengingat | 120 dan 145 | 3 dan 5 | Tersirat kuat |
| Rekomendasi AI dan deteksi anomali | 92 dan 1 | 5 dan 0 | Hanya tersirat dari keluhan |
| Dosis otomatis | 76 | 1 | Tersirat, tetapi dibantah 189 rekaman anti-otomatisasi |

Orang meminta **jawaban dan panduan**. Kata "AI" dan "deteksi anomali" hampir tidak pernah disebut.

### 7.7 Persona

| Persona | Jumlah (porsi) | Ciri utama | Relevansi bagi HYCANE |
|---|---|---|---|
| **P0 Pemula yang Mengaku Pemula** | 5.026 (16%) | 100% menyebut diri pemula; bertanya dan berterima kasih; butuh edukasi; belum ada sinyal beli | Calon pengguna starter kit; perlu dipandu |
| **P1 Evaluator Hemat / Perakit DIY** | 16.374 (53%) | Membandingkan sistem dan merek, banyak bicara harga dan DIY, memberi saran, membahas sensor; memegang hampir semua sinyal beli dan sebagian besar bantahan | Calon pembeli paling nyata sekaligus pengkritik paling keras |
| **P2 Pembelajar yang Terinspirasi Tutorial** | 4.867 (16%) | Mayoritas YouTube, 48% positif, inspirasi dan edukasi, hampir tanpa keluhan dan sinyal beli | Audiens konten dan workshop, belum pembeli |
| **P3 Penanam yang Sedang Bermasalah** | 4.847 (16%) | 96% memecahkan masalah; tanaman sakit; paling negatif (33%); meminta diagnosis | Paling cocok dengan solusi HYCANE; kandidat ideal uji coba |

**Peringatan:** persona ini **rapuh**. Jika data per platform disamakan, pengelompokannya cukup berubah (ARI 0,14). Pakai sebagai hipotesis untuk diuji lewat survei, bukan fakta.

### 7.8 Harga

| Sinyal harga | Jumlah | Persen |
|---|---|---|
| Bahasa murah, hemat, atau DIY | 2.256 | 2,48% |
| Menyebut angka harga | 1.752 | 1,92% |
| Bertanya harga | 1.156 | 1,27% |
| Langganan, pod, atau isi ulang | 859 | 0,94% |
| Bahasa premium atau "worth it" | 455 | 0,50% |
| Keberatan harga ("kemahalan") | 292 | 0,32% |

- **Pembicaraan harga di Indonesia** berkisar pada harga komponen dan nutrisi (umumnya sekitar Rp10 ribu sampai Rp100 ribu per barang), modal instalasi usaha kecil (sekitar Rp2 juta sampai Rp8 juta), dan apakah lebih murah meracik AB mix sendiri.
- **Pembicaraan harga berbahasa Inggris** membandingkan smart garden (AeroGarden, Gardyn, Click & Grow) dengan rakitan ember atau kontainer, dan mengkritik pod benih yang mahal.
- **Tidak ada angka kesediaan membayar yang bisa disimpulkan.** Harga Rp910.000 harus diuji langsung.

### 7.9 Keberlanjutan dan ampas tebu

| Hal | Hasil |
|---|---|
| Ada sinyal keberlanjutan apa pun | 7,3% |
| Positif terhadap keberlanjutan | 0,65% |
| Skeptis | 113 rekaman (terutama soal listrik) |
| Dari rekaman bersinyal beli, yang menyebut keberlanjutan | 10,7% |
| Dari rekaman bersinyal beli, yang menyebut harga atau biaya | 33,2% |
| Ampas tebu disebut dalam suara pelanggan | 18 dari 91.068 |
| Semua sebutan ampas tebu yang ditemukan | 152; hanya 19 terkait media tanam atau kompos, sisanya piring, kemasan, energi, kertas, pakan |
| Media tanam yang benar-benar dibicarakan | Kelapa (cocopeat) 1.049, rockwool 1.044, clay pebbles 715, spons 687, perlit 572, gambut 295 |
| Keluhan terkait rockwool | Sekitar 160 |

### 7.10 Bukti akademik dan pakar

**Bukti kuat (pelanggan, akademik, dan pakar sepakat):**

- pH dan EC/TDS adalah variabel utama yang perlu dikendalikan. Penyuluhan universitas menyarankan pengecekan mingguan. Penelitian di iklim tropis menemukan selada terbaik pada EC sekitar 0,9 sampai 1,4 dS/m.
- Busuk akar adalah kegagalan paling umum dan dipicu air hangat yang kurang oksigen.
- Pemula butuh edukasi terstruktur. Studi kasus Edufarming di Sulawesi Selatan dan studi rumah tangga di Surabaya mendukung ini.
- Biaya adalah penghambat. Studi di Cape Town dan Surabaya mendukung ini, dan penyuluhan Illinois menyarankan sistem pasif murah.

**Yang bertentangan atau perlu hati-hati:**

- Pakar UF/IFAS dan sebuah tinjauan ilmiah 2023 mengingatkan bahwa sensor dan dosis otomatis berbasis EC punya keterbatasan dan bisa memboroskan nutrisi.
- Studi petani milenial di Malang menemukan kesadaran lingkungan berpengaruh pada adopsi, tetapi percakapan publik jarang menyebutnya. Hal ini perlu diuji lewat survei.

**Celah besar:** **tidak ada penelitian** dalam 677 publikasi yang menguji ampas tebu sebagai media hidroponik air. Yang ada hanya pembanding, yaitu sabut kelapa dicampur bagasse untuk tomat tanpa tanah, dan limbah kurma yang hasilnya setara rockwool.

---

## 8. Uji Asumsi HYCANE

| Kode | Asumsi | Hasil | Penjelasan singkat |
|---|---|---|---|
| H01 | Penanam rumahan perkotaan adalah segmen inti | **Didukung sebagian** | Skala rumahan atau hobi mendominasi, tetapi ruang sempit adalah konteks, bukan keluhan |
| H02 | Pemula adalah segmen inti dengan masalah berulang | **Didukung** | 84% dari yang menyebut pengalaman adalah pemula; keluhan pengetahuan dan kesehatan tanaman masuk lima besar |
| H03 | Usia 20 sampai 40 tahun | **Bukti belum cukup** | Hanya sekitar 10 rekaman menyebut usia; usia tidak boleh ditebak dari gaya tulisan |
| H04 | Indonesia, prioritas Jawa | **Didukung sebagian** | Komunitas belajar hidroponik berbahasa Indonesia aktif (30.703 rekaman); prioritas Jawa tidak bisa diuji |
| H05 | Harga kelas menengah dapat diterima | **Bukti belum cukup** | Tidak ada data kesediaan membayar; sinyal hemat dan DIY kuat (risiko) |
| H06 | Tertarik teknologi atau smart farming | **Didukung sebagian** | Ada, tetapi ceruk (sekitar 4%); sensor sering dibicarakan negatif |
| H07 | Keberlanjutan adalah alasan membeli | **Tidak didukung** | Jarang disebut dan jauh kalah dari harga |
| H08 | Sekolah, kampus, dan komunitas sebagai pembeli | **Bukti belum cukup** | Kurang dari 1%; tetapi cocok sebagai saluran edukasi |
| H09 | B2B (urban farm, restoran, hotel, UMKM) | **Didukung sebagian** | UMKM hidroponik kecil masuk akal; restoran dan hotel hampir tidak muncul |
| H10 | Ampas tebu bernilai bagi pelanggan | **Tidak didukung** | Hampir tidak disebut; nilai rekayasa dan cerita keberlanjutan, bukan permintaan pelanggan |
| H11 | Pengguna ingin pemantauan pH, EC, suhu, dan air | **Didukung** (pH dan EC) | Diminta eksplisit di 6 platform; suhu dan ketinggian air hanya tersirat |
| H12 | Pengguna ingin rekomendasi AI dan deteksi anomali | **Didukung sebagian** | Yang diinginkan adalah diagnosis dan jawaban, bukan "AI" |
| H13 | Aplikasi dan langganan diterima | **Bukti belum cukup** | Ada keluhan pod, langganan, dan aplikasi yang tidak andal |

Rincian angka per hipotesis: `outputs/tables/hypothesis_metrics.json` dan `outputs/tables/hypothesis_validation.csv`.

---

## 9. Bukti yang Melemahkan Konsep HYCANE

Bagian ini sengaja dicari supaya riset tidak hanya "membenarkan" ide HYCANE.

| Bantahan | Jumlah rekaman | Platform | Contoh (diparafrasakan) |
|---|---|---|---|
| Tidak perlu otomatisasi, lebih suka sistem pasif | 189 | 8 | Penanam senior bilang sistem sumbu atau Kratky paling andal dan bisa ditinggal berminggu-minggu |
| Lebih murah bikin sendiri | 42 | 7 | "Saya bisa bikin ini dengan sebagian kecil harganya" |
| Kembali ke tanah | 33 | 6 | Berhenti hidroponik karena capek mengejar pH dan suhu air tanpa chiller |
| Skeptis keberlanjutan | 30 | 6 | "Boros listrik ya kalau pakai pompa terus?" |
| Tidak suka langganan atau pod | 21 | 7 | Pod benih sekitar 5 dolar per buah dianggap pemerasan; lebih suka tanam benih sendiri |
| Tidak suka aplikasi | 8 | 2 | Aplikasi tidak mengirim peringatan kecuali dibuka; WiFi sering putus |
| Tidak percaya sensor | 8 | 3 | Probe pH kering, papan sinyal sulit dikalibrasi |
| Skeptis AI | 3 | 3 | Pemilik usaha ragu AI memberi perbaikan nyata |

Bantahan dari luar data pelanggan:

1. AeroGarden diumumkan tutup akhir 2024 lalu kembali 2025, yang menunjukkan bisnis smart garden rentan.
2. Pakar menyebut dosis otomatis berbasis EC tidak presisi.
3. Belum ada bukti ilmiah kinerja ampas tebu sebagai media hidroponik air.

**Bantahan terkuat:** budaya hemat, DIY, dan sistem pasif. Banyak penghobi percaya ember, aerator, dan metode Kratky sudah cukup, dan kit terpadu dianggap kemahalan.

**Sisi baiknya:** bantahan "kembali ke tanah" justru membuktikan masalahnya nyata. Orang berhenti karena masalah pH dan suhu, persis masalah yang ingin diselesaikan HYCANE.

---

## 10. Rekomendasi untuk HYCANE

1. **Ubah pesan utama** dari "kit hidroponik pintar IoT dan AI berbahan ampas tebu" menjadi **"kit terpandu supaya tanaman pemula tidak mati"**.
2. **Fitur inti:** pemantauan pH dan TDS/EC ditambah panduan "apa yang harus dilakukan sekarang" dalam bahasa sederhana, ditambah diagnosis gejala seperti daun kuning dan akar busuk. AI cukup disebut sebagai mesin di balik layar, bukan jualan utama.
3. **Edukasi dan komunitas sebagai saluran utama:** kerja sama dengan kreator YouTube hidroponik Indonesia, workshop, dan panduan langkah demi langkah di aplikasi.
4. **Rancang untuk iklim tropis:** pemantauan suhu air, panduan saat panas dan hujan, pompa hemat listrik, dan informasi konsumsi listrik yang transparan.
5. **Media ampas tebu:**
   - uji di laboratorium dulu (perkecambahan, pertumbuhan akar, stabilitas pH dibanding rockwool dan spons);
   - jual sebagai media yang praktis (tidak gatal, mudah dibuang, hasil konsisten);
   - jadikan keberlanjutan sebagai bukti pendukung.
6. **Harga:**
   - bandingkan dengan biaya rakit sendiri ditambah kerugian gagal panen;
   - sediakan versi awal yang lebih murah, misalnya tanpa sensor dengan modul sensor opsional;
   - isi ulang media dan nutrisi harus terbuka dan harganya transparan.
7. **Jangan wajibkan langganan:** kit harus tetap berfungsi tanpa langganan dan tanpa koneksi internet. Peringatan harus tetap muncul tanpa membuka aplikasi.
8. **B2B:** mulai dari UMKM hidroponik kecil yang butuh hemat waktu pemantauan, bukan hotel atau restoran.
9. **Perbaiki BMC:**
   - Customer Segments: pemula sebagai segmen utama; usia dan pendapatan ditandai "perlu validasi".
   - Value Proposition: "lebih sedikit tanaman gagal".
   - Channels: kreator YouTube dan workshop.
   - Revenue Streams: kit bertingkat, isi ulang terbuka, workshop; langganan premium ditunda sampai retensi terbukti.

Teks siap tempel untuk proposal (Bahasa Indonesia): `outputs/proposal_ready_insights.md`.

---

## 11. Yang Belum Diketahui dan Harus Diuji Berikutnya

| Yang perlu dibuktikan | Cara menguji | Sampel | Ukuran keberhasilan | Aturan keputusan |
|---|---|---|---|---|
| Pemula memilih kit terpandu dibanding DIY | Uji konsep 3 penawaran | 150 pemula atau calon pemula (Jawa dan 1 kota luar Jawa) | Pilihan pertama | Lanjut bila minimal 30% memilih HYCANE dengan sensor |
| Harga Rp910.000 diterima | Survei harga Van Westendorp dan Gabor-Granger | 150 orang yang sama | Rentang harga wajar | Pertahankan bila masuk rentang; bila tidak, buat versi bertingkat |
| Media ampas tebu setara rockwool | Uji laboratorium | 3 jenis tanaman × 30 sel × 3 media | Persentase berkecambah, hari berakar, perubahan pH | Klaim hanya bila tidak lebih buruk dari rockwool |
| Pemantauan mengurangi kegagalan | Uji coba di rumah 4 minggu | 20 rumah tangga | Tanaman bertahan hidup, panen, pemakaian aplikasi di hari ke-30 (target minimal 60%), deviasi pH maksimal 0,2 | Lanjut bila tanaman bertahan naik minimal 20 poin persen |
| Keberlanjutan menarik pembeli | Uji A/B iklan | Minimal 1.000 tayangan per versi | Klik dan pendaftaran | Pakai pesan yang menang |
| UMKM mau membayar | Wawancara | 10 UMKM hidroponik | Kesediaan ikut uji coba berbayar | Bangun paket B2B bila minimal 4 setuju |
| Demografi sebenarnya | Pertanyaan saringan di survei | Bagian dari survei | Usia, tempat tinggal, rentang pendapatan | Ganti asumsi dengan data terukur |

---

## 12. Keterbatasan Riset

Keterbatasan ini perlu disampaikan secara jujur di proposal:

1. **Bukan survei populasi.** Ini percakapan publik yang dipilih sendiri oleh penulisnya. Tidak bisa dipakai untuk menghitung ukuran pasar, persentase penduduk, atau kesediaan membayar.
2. **Data Indonesia hampir seluruhnya dari YouTube** (sekitar 99,7%). Porsinya juga dipengaruhi pilihan kata kunci berbahasa Indonesia. Instagram, TikTok, grup Facebook, WhatsApp, Kaskus, dan marketplace tidak bisa diakses.
3. **YouTube mendominasi** (60% suara pelanggan). Platform berbahasa Inggris cenderung berisi penghobi melek teknologi di Amerika dan Eropa.
4. **Reddit diambil lewat arsip pihak ketiga** (Arctic Shift), bukan API resmi.
5. **Ada batasan pengambilan sampel:** maksimal 100 postingan per kuartal per subreddit, 300 utas komentar Reddit, 300 utas per video YouTube, 50 jawaban per utas forum, dan r/DWC dihentikan di tengah jalan karena didominasi ganja.
6. **Konteks ganja** hanya ditandai dari kata yang eksplisit. Utas yang tersirat masih mungkin lolos.
7. **Label berbasis aturan akurasinya sedang** (lihat 6.9). Pakai urutannya, bukan angka mutlaknya.
8. **Label pembanding validasi dibuat AI, bukan manusia.**
9. **Model sentimen dilatih dari tweet.** Teks teknis panjang sering dilabeli ambigu atau netral.
10. **Persona adalah segmen percakapan, bukan orang**, dan statistiknya rapuh.
11. **Lokasi hampir tidak diketahui** (hanya 1,2% rekaman punya petunjuk lokasi eksplisit).
12. **Bukti akademik dibaca sampai abstrak saja.** Status "jurnal" di OpenAlex tidak menjamin kualitas tinjauan sejawat.
13. **Data lama** (sejak 2002) mungkin membahas produk dan harga yang sudah tidak berlaku.

Rincian lengkap: `outputs/limitations.md`.

---

## 13. Cara Membaca Angka dalam Riset Ini

- **"Rekaman"** adalah satu postingan atau satu komentar.
- **"Gold"** adalah rekaman yang lolos semua saringan (relevan, bukan spam, bukan duplikat).
- **"Suara pelanggan" (customer voice)** adalah gold tanpa konteks ganja dan tanpa berita atau promosi. Ini **penyebut utama persentase** (91.068).
- **Persentase kecil itu wajar.** Misalnya "kesehatan tanaman 5,2%" berarti 5,2% dari semua komentar menyebut masalah kesehatan tanaman secara jelas. Banyak komentar hanya berupa "terima kasih" atau pertanyaan singkat, jadi angka kecil tetap berarti ribuan orang.
- **Urutan lebih penting daripada angka mutlak**, karena aturan deteksi keluhan tidak sempurna tetapi urutannya stabil.
- **"Muncul di 8 platform"** artinya bukan hanya satu komunitas yang membicarakannya. Ini tanda bukti yang lebih kuat.
- **Tingkat bukti (E0 sampai E5):**
  - E1: satu cerita saja.
  - E2: berulang di satu platform.
  - E3: berulang di banyak platform.
  - E4: riset primer.
  - E5: jurnal atau panduan resmi.
- **Tingkat insight (1 sampai 5):** 3 berarti lintas platform; 4 berarti didukung akademik atau pakar juga; 5 berarti sudah diuji langsung. Belum ada temuan di level 5 karena riset primer belum dilakukan.

---

## 14. Etika, Privasi, dan Aturan Akses

- **Hanya data publik.** Tidak ada grup privat, akun privat, atau pesan pribadi.
- **Tidak ada pembobolan.** Tidak membobol CAPTCHA, login, paywall, robots.txt, atau sistem anti-bot. Platform yang menolak dicatat sebagai celah, bukan diakali.
- **Tidak ada data palsu.** Tidak ada komentar, survei, kutipan, atau angka yang dikarang.
- **Nama akun tidak disimpan.** Setiap penulis diganti kode acak (hash) yang tidak bisa dikembalikan ke nama aslinya.
- **Kunci API** disimpan di file `.env` yang tidak ikut ke Git dan tidak pernah dicetak di log. Kunci YouTube sempat ditempel di percakapan, jadi sebaiknya dibuat ulang (regenerate) setelah proyek selesai.
- **Di laporan, contoh komentar diparafrasakan** agar tidak menyorot individu.

---

## 15. Struktur Folder dan File Penting

```
hycane-scraping/
├── README.md                          <- dokumen ini
├── README_SPESIFIKASI_AWAL.md         <- README spesifikasi paket riset (asli)
├── CLAUDE.md, MASTER_PROMPT.md, 00_ sampai 22_*.md   <- spesifikasi riset
├── run_pipeline.sh                    <- menjalankan ulang seluruh proses
├── requirements.txt                   <- daftar paket Python
├── .env.example                       <- template kunci API (isi ke .env)
├── config/                            <- semua aturan dan bobot
│   ├── project.yaml                   <- info proyek dan daftar hipotesis
│   ├── source_targets.yaml            <- sumber data dan batasannya
│   ├── queries.yaml                   <- kata kunci pencarian
│   ├── filters.yaml                   <- relevansi, eksklusi, spam, duplikat
│   ├── taxonomy.yaml                  <- pola keluhan, niat, fitur, harga, kontradiksi
│   ├── hycane_mapping.yaml            <- keluhan ke fitur ke komponen HYCANE
│   ├── academic_curated.yaml          <- rangkuman 14 publikasi
│   └── synthesis_notes.yaml           <- nama topik, persona, putusan hipotesis
├── src/                               <- kode program
│   ├── collectors/                    <- pengumpul data per platform
│   ├── normalization/                 <- RAW ke BRONZE
│   ├── quality/                       <- BRONZE ke SILVER (pembersihan, spam, duplikat)
│   ├── nlp/                           <- sentimen, topik, aturan, validasi
│   ├── persona/                       <- pengelompokan persona
│   ├── evidence/                      <- bukti akademik dan pakar
│   ├── reporting/                     <- tabel, sintesis, laporan
│   └── visualization/                 <- grafik dan dashboard
├── data/
│   ├── raw/                           <- data mentah asli (tidak pernah diubah)
│   ├── bronze/, silver/               <- data antara
│   ├── gold/                          <- DATA FINAL
│   │   ├── hycane_social_listening_gold.parquet / .csv / .jsonl
│   │   ├── academic_evidence.parquet
│   │   └── expert_evidence.parquet / .csv
│   ├── annotation/                    <- sampel validasi dan antrean anotasi manusia
│   ├── manifests/                     <- catatan proses, model, duplikat
│   └── logs/                          <- buku catatan permintaan
├── outputs/
│   ├── final_report.md                <- LAPORAN LENGKAP (bahasa Inggris)
│   ├── executive_summary.md           <- ringkasan eksekutif
│   ├── proposal_ready_insights.md     <- TEKS SIAP TEMPEL PROPOSAL (Bahasa Indonesia)
│   ├── hycane_strategy_implications.md <- prioritas fitur, perubahan BMC
│   ├── persona_report.md              <- detail 4 persona
│   ├── academic_expert_synthesis.md   <- rangkuman bukti ilmiah dan pakar
│   ├── pricing_research_gaps.md       <- temuan harga dan hipotesis harga
│   ├── methodology.md, limitations.md, reproducibility.md
│   ├── source_inventory.md, environment_audit.md, source_access_audit.md
│   ├── collection_completion_report.md, data_quality_report.md
│   ├── FINAL_STATUS.md, final_manifest.json, qa_results.txt
│   ├── tables/                        <- semua tabel sumber angka
│   ├── figures/                       <- 20 grafik (PNG dan SVG)
│   └── dashboard/index.html           <- DASHBOARD INTERAKTIF
└── tests/test_integrity.py            <- 42 tes kualitas
```

### File yang paling sering dibutuhkan

| Kebutuhan | Buka file ini |
|---|---|
| Ingin cepat paham hasilnya | `README.md` (bagian 1 dan 2) atau `outputs/executive_summary.md` |
| Menulis proposal | `outputs/proposal_ready_insights.md` |
| Melihat grafik secara interaktif | `outputs/dashboard/index.html` |
| Mengambil grafik untuk slide atau proposal | `outputs/figures/` |
| Mengecek asal sebuah angka | `outputs/tables/` |
| Membaca semua detail | `outputs/final_report.md` |

### Daftar grafik

| File | Isi |
|---|---|
| 01_platform_coverage | Jumlah suara pelanggan per platform |
| 02_source_family_coverage | Corong data dari terkumpul sampai gold |
| 03_timeline | Jumlah percakapan per tahun |
| 04_sentiment_by_platform | Sentimen per platform |
| 05_sentiment_by_topic | Sentimen per topik |
| 06_top_pain_points | Frekuensi keluhan |
| 07_painpoint_frequency_severity | Frekuensi dibanding keparahan keluhan |
| 08_intent_distribution, 08b_intent_by_platform | Niat percakapan |
| 09_feature_demand | Fitur yang disebut dan diminta |
| 10_persona_distribution | Ukuran persona |
| 11_persona_painpoints | Persona × keluhan |
| 12_persona_features | Persona × fitur |
| 13_language_distribution | Bahasa |
| 14_geography_explicit | Lokasi (hanya yang eksplisit) |
| 15_platform_topic_heatmap | Platform × topik |
| 16_evidence_strength | Tingkat bukti |
| 17_hycane_feature_mapping | Keluhan ke komponen HYCANE |
| 18_contradictions | Bukti yang membantah asumsi |
| 19_saturation | Kejenuhan tema |

---

## 16. Cara Menjalankan Ulang

### Persiapan (sekali saja)

```bash
cd /Users/macbookpro/Projects/hycane-scraping
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env      # lalu isi kunci API yang dimiliki, misalnya YOUTUBE_API_KEY
```

### Menjalankan

```bash
./run_pipeline.sh process   # memproses ulang dari data mentah yang sudah ada (tanpa mengunduh lagi)
./run_pipeline.sh collect   # melanjutkan pengumpulan data (yang sudah selesai dilewati)
./run_pipeline.sh all       # keduanya
```

### Membuka dashboard

```bash
open outputs/dashboard/index.html
```

Dashboard butuh koneksi internet untuk memuat pustaka grafik.

### Menjalankan tes kualitas

```bash
.venv/bin/python -m pytest -q tests/
```

### Catatan

- Angka acak dikunci (seed 42), sehingga hasil pemrosesan ulang sama.
- Hasil model disimpan di cache, sehingga pemrosesan ulang cepat.
- Mengumpulkan ulang dari internet akan menghasilkan data yang sedikit berbeda karena postingan baru muncul dan postingan lama terhapus. Memproses ulang data mentah yang tersimpan akan menghasilkan angka yang sama.
- Kalau kunci API untuk platform lain (misalnya Reddit resmi atau X) ditambahkan ke `.env`, pengumpul yang sesuai bisa diaktifkan.

---

## 17. Glosarium

| Istilah | Arti sederhana |
|---|---|
| Social listening | "Mendengarkan" percakapan publik di internet untuk memahami pendapat dan masalah orang |
| API | Pintu resmi yang disediakan platform agar program bisa mengambil data secara teratur |
| robots.txt | File di sebuah situs yang memberi tahu program bagian mana yang boleh dan tidak boleh diakses |
| RAW, BRONZE, SILVER, GOLD | Tahapan data dari mentah sampai siap analisis |
| Deduplikasi | Membuang data yang sama atau hampir sama supaya satu suara tidak dihitung berkali-kali |
| Embedding | Mengubah kalimat menjadi deretan angka yang mewakili maknanya, supaya komputer bisa membandingkan kemiripan makna |
| Sentimen | Nada tulisan: positif, netral, negatif, campuran, atau ambigu |
| Pain point | Keluhan atau kesulitan yang dialami |
| Intent | Niat atau tujuan seseorang saat menulis |
| Persona | Gambaran tipe pelanggan |
| Topic modeling | Cara komputer menemukan topik dengan mengelompokkan teks yang mirip |
| Validasi | Mengecek seberapa sering label komputer cocok dengan label pembanding |
| Akurasi | Persentase label yang benar |
| Presisi | Dari yang ditandai komputer, berapa persen yang benar |
| Recall | Dari yang seharusnya tertangkap, berapa persen yang berhasil ditangkap |
| Macro F1 | Nilai gabungan presisi dan recall yang dirata-ratakan antar kelas (0 sampai 1, makin tinggi makin baik) |
| Korelasi peringkat (Spearman) | Seberapa mirip dua urutan (1 berarti identik) |
| Cramér's V | Ukuran seberapa besar perbedaan antar kelompok (0 berarti tidak ada beda, makin mendekati 1 makin besar) |
| ARI | Ukuran seberapa mirip dua hasil pengelompokan (1 berarti sama persis, mendekati 0 berarti sangat berbeda) |
| Silhouette | Ukuran seberapa jelas kelompok-kelompok terpisah satu sama lain |
| Triangulasi | Membandingkan bukti dari beberapa sumber berbeda untuk melihat apakah saling menguatkan |
| pH | Tingkat keasaman air nutrisi; idealnya sekitar 5,5 sampai 6,5 untuk kebanyakan tanaman hidroponik |
| TDS, EC, ppm | Ukuran kepekatan nutrisi dalam air |
| AB mix | Nutrisi hidroponik dua bagian (A dan B) yang populer di Indonesia |
| Kratky, sistem sumbu (wick) | Sistem hidroponik pasif tanpa pompa dan listrik |
| NFT, DFT, rakit apung, DWC | Jenis-jenis sistem hidroponik dengan aliran atau genangan air |
| Rockwool | Media tanam dari serat batuan yang umum dipakai; tidak mudah terurai |
| Bagasse | Ampas tebu |
| BMC | Business Model Canvas, peta 9 blok model bisnis |
| Van Westendorp, Gabor-Granger | Metode survei untuk mengukur rentang harga yang dianggap wajar |
