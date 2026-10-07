# Sisipan Siap Pakai untuk Proposal BPC RISE 2026 (HYCANE)

Teks di bawah ini ditulis untuk disalin ke proposal. Setiap angka merujuk ke tabel di `outputs/tables/`. Sebut data ini sebagai **hasil social listening (studi eksploratif data publik daring)**, bukan survei populasi. Konversi ke gaya EYD final tetap tanggung jawab tim.

---

## 1. Latar Belakang — bukti dari percakapan publik
Dalam korpus publik yang diamati, terkumpul 93.125 unggahan dan komentar relevan dari 8 platform: YouTube, Reddit, forum GardenWeb, Mastodon, Hacker News, Bluesky, Lemmy, dan Stack Exchange. Rentang waktunya 2002–2026, dengan 30.703 komentar berbahasa Indonesia (sumber: `platform_coverage.csv`, `analysis_results.json`).

Hambatan yang paling sering muncul adalah:
- kesehatan tanaman (akar busuk, daun menguning, layu, hama);
- pengelolaan nutrisi;
- pengendalian pH;
- kerusakan peralatan;
- kurangnya pengetahuan pemula.

Urutan prioritas ini stabil pada delapan uji sensitivitas, dengan korelasi peringkat minimum 0,96 (`pain_point_summary.csv`, `pain_point_sensitivity_pct.csv`). Biaya menjadi keluhan kedua yang paling sering disebut, tetapi tingkat keparahannya lebih rendah.

## 2. Permasalahan pelanggan (masalah → bukti → dampak)
- **Masalah:** pengguna, terutama pemula, sulit mengetahui kondisi air nutrisi (pH, kepekatan/TDS-EC, suhu) sebelum tanaman rusak.
- **Bukti:** keluhan kesehatan tanaman muncul pada 4.754 rekaman dan tersebar di 8 platform. Keluhan nutrisi, pH, dan EC/TDS bersama-sama mencapai sekitar 2.500 rekaman (`pain_point_summary.csv`). Panduan penyuluhan universitas juga menyarankan pemantauan pH/EC mingguan dan menyebut air yang hangat dan kurang oksigen sebagai pemicu utama busuk akar (`academic_expert_synthesis.md`: EX001–EX004).
- **Dampak:** muncul percakapan tentang menyerah dan kembali ke tanah karena "mengejar pH" dan suhu air (`contradiction_register.csv`: SOIL_PREFERENCE).

## 3. Persona pelanggan (berbasis bukti, perlu divalidasi)
- **Siapa:** pemula hidroponik rumahan. Di antara rekaman yang menyebutkan tingkat pengalaman, 84% adalah pemula atau belum pernah mencoba (`hypothesis_metrics.json` H02).
- **Konteks:** belajar terutama dari tutorial YouTube berbahasa Indonesia. Topik terbesar dalam percakapan Indonesia adalah ucapan terima kasih atas tutorial dan pertanyaan langsung kepada kreator (`topic_summary.csv`).
- **Pekerjaan yang ingin diselesaikan:** memulai sistem yang berhasil hingga panen pertama.
- **Kesulitan:** tanaman layu atau menguning, takaran AB mix dan ppm, panas dan hujan.
- **Sinyal pembelian:** pertanyaan "beli di mana" dan "harga berapa" serta pembahasan modal (`topic_summary.csv`, topik "Buying: price, where to buy, start-up capital"; 2.733 rekaman).
- **Relevansi fitur:** pemantauan pH/TDS, panduan langkah demi langkah, dan diagnosis masalah.

> Catatan: usia 20–40 tahun **tidak dapat divalidasi** dari data publik (`hypothesis_validation.csv` H03). Cantumkan sebagai asumsi yang akan diuji melalui survei.

## 4. Proposisi nilai (masalah tervalidasi → respons HYCANE → hasil bagi pengguna)
Masalah yang paling sering dan paling berat adalah tanaman rusak karena kondisi air yang tidak terpantau. HYCANE menjawabnya dengan pemantauan pH dan TDS/EC serta panduan "apa yang harus dilakukan sekarang" dalam bahasa sederhana. Hasil yang dituju adalah lebih sedikit tanaman gagal dan panen pertama yang lebih percaya diri.

Fitur ini termasuk yang paling banyak diminta secara eksplisit:
- edukasi/tutorial: 228 permintaan eksplisit di 8 platform;
- pemantauan TDS/EC: 46 permintaan di 6 platform;
- pemantauan pH: 31 permintaan di 6 platform.

Sumber: `feature_demand.csv`.

> Hindari klaim "panen dijamin" atau "budidaya otomatis penuh". Pakar mengingatkan bahwa sensor dan dosis otomatis berbasis EC tetap memiliki keterbatasan (EX005; W4388723157).

## 5. Fitur produk (prioritas berbasis bukti)
1. Pemantauan pH dan TDS/EC dengan rekomendasi tindakan — permintaan eksplisit.
2. Mode pemula, perpustakaan edukasi, dan komunitas — permintaan eksplisit paling besar.
3. Diagnosis gejala (daun kuning, akar busuk) — permintaan eksplisit; keluhan nomor 1.
4. Pemantauan suhu air dan panduan cuaca panas/hujan — topik khas percakapan Indonesia.
5. Pengingat dan peringatan ketinggian air yang tetap berfungsi tanpa membuka aplikasi.

Fitur "AI" disampaikan sebagai **diagnosis dan rekomendasi**, bukan sebagai jargon. Dosis otomatis tidak dimasukkan ke MVP karena ada preferensi kuat terhadap sistem pasif (189 rekaman ANTI_AUTOMATION di 8 platform).

## 6. Media tanam ampas tebu dan narasi keberlanjutan
- **Bukti:** ampas tebu hampir tidak dibicarakan sebagai media tanam oleh pengguna, hanya 18 dari 91.068 rekaman. Percakapan publik tentang bagasse didominasi topik kemasan, peralatan makan, dan energi (`analysis_results.json` → bagasse_discourse).
- **Yang lebih sering dikeluhkan:** rockwool, terkait rasa gatal, pH, dan limbah (sekitar 160 rekaman).
- **Bahasa keberlanjutan:** sinyal positif keberlanjutan hanya 0,65% dari percakapan. Pada rekaman bersinyal pembelian, keberlanjutan muncul pada 11%, sedangkan harga/biaya muncul pada 33% (`hypothesis_metrics.json` H07).
- **Kalimat aman untuk proposal:** "Media tanam ampas tebu diposisikan sebagai media yang praktis dan rendah limbah, sekaligus bukti penerapan ekonomi sirkular. Keunggulan kinerjanya dibanding rockwool akan dibuktikan melalui uji laboratorium (perkecambahan, pertumbuhan akar, stabilitas pH) sebelum diklaim."
- **Tema RISE:** keberlanjutan tetap relevan untuk tema kompetisi. Posisikan sebagai nilai pendukung dan bukti dampak, bukan alasan utama pelanggan membeli.

## 7. Strategi pemasaran
- **Pesan:** "Panen pertamamu, dipandu langkah demi langkah", "Tahu masalahnya sebelum tanaman mati", dan "Lebih hemat daripada gagal panen". Ini wilayah pesan untuk diuji, bukan slogan final.
- **Saluran utama:** kemitraan dengan kreator YouTube hidroponik Indonesia dan workshop. YouTube adalah arena belajar terbesar dalam data, dengan 54.622 komentar dari 896 video (`platform_coverage.csv`). Instagram, TikTok, dan Facebook tidak dapat diakses dalam studi ini sehingga efektivitasnya belum teruji.
- **Ajakan bertindak:** kelas atau komunitas gratis, lalu starter kit.

## 8. Business Model Canvas — blok yang berubah
| Blok | Perubahan |
|---|---|
| Customer Segments | Pemula rumahan sebagai segmen utama; usia dan pendapatan ditandai "perlu validasi"; B2B dimulai dari UMKM hidroponik kecil |
| Value Propositions | Utama: "lebih sedikit tanaman gagal"; ampas tebu sebagai media praktis dan rendah limbah |
| Channels | Tambahkan kreator YouTube dan workshop sebagai saluran utama |
| Customer Relationships | Panduan dalam aplikasi, komunitas, dan dukungan diagnosis |
| Revenue Streams | Kit bertingkat; refill media/nutrisi yang terbuka (tanpa penguncian); langganan premium ditunda sampai retensi terbukti |
| Key Activities & Partners | Uji laboratorium media dan kemitraan konten |

Rincian lengkap: `hycane_strategy_implications.md`.

## 9. Rencana validasi
| Hipotesis | Uji | Sampel | Metrik | Aturan keputusan |
|---|---|---|---|---|
| Pemula memilih kit terpandu dibanding DIY | Uji konsep 3 penawaran | 150 responden | Preferensi pilihan pertama | Lanjut bila ≥ 30% memilih HYCANE |
| Harga Rp910.000 diterima | Van Westendorp dan Gabor-Granger | 150 | Rentang harga wajar | Pertahankan bila berada dalam rentang; bila tidak, buat tier |
| Media ampas tebu setara rockwool | Uji laboratorium | 3 tanaman × 30 sel × 3 media | Perkecambahan, hari berakar, drift pH | Klaim hanya bila tidak lebih buruk |
| Pemantauan menurunkan kegagalan | Pilot rumah 4 minggu | 20 rumah tangga | Kelangsungan hidup tanaman; retensi aplikasi D30 | Lanjut bila kelangsungan hidup naik ≥ 20 poin persen |
| Keberlanjutan sebagai pendorong | Uji A/B iklan | ≥ 1.000 tayangan per varian | CTR | Gunakan bingkai pesan yang menang |

## 10. Kalimat metodologi untuk lampiran
"Analisis pasar diperkuat dengan studi social listening terhadap 136.019 objek publik daring dari 8 platform. Data disaring menjadi 93.125 rekaman relevan melalui deduplikasi berlapis, penyaringan spam, dan deteksi bahasa. Data dianalisis dengan model sentimen multibahasa XLM-R (akurasi 3-kelas 0,72 dan 0,84 untuk teks berbahasa Indonesia pada sampel validasi 420 rekaman berlabel referensi LLM), pemodelan topik BERTopic, serta taksonomi keluhan, intensi, dan fitur. Hasil dibandingkan dengan 677 publikasi akademik (OpenAlex) dan 7 sumber pakar. Studi ini bersifat eksploratif dan tidak mewakili populasi; validasi primer dijadwalkan pada tahap berikutnya."
