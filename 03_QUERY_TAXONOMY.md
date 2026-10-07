# 03 Query Taxonomy

Build a systematic multilingual query space. Start with Bahasa Indonesia and English. Add Malay, Spanish, and Portuguese when data quality and model support are adequate.

## Query clusters
A Core hydroponics: `hidroponik`, `tanaman hidroponik`, `hydroponics`, `hydroponic gardening`

B Beginner: `hidroponik pemula`, `belajar hidroponik`, `mulai hidroponik`, `beginner hydroponics`

C Interest: `pengen hidroponik`, `mau hidroponik`, `ingin hidroponik`, `hydroponics at home`, `want to start hydroponics`

D Failure/frustration: `hidroponik gagal`, `tanaman hidroponik mati`, `daun kuning hidroponik`, `hydroponic failure`, `hydroponic problems`

E Nutrients: `pH hidroponik`, `TDS hidroponik`, `EC hidroponik`, `ppm hidroponik`, `nutrisi hidroponik`, `hydroponic pH`, `hydroponic EC`

F Water/environment: `air hidroponik`, `suhu air hidroponik`, `oksigen hidroponik`, `water level hydroponic`, `water temperature hydroponics`

G IoT/automation: `sensor hidroponik`, `monitor hidroponik`, `otomatis hidroponik`, `IoT hidroponik`, `smart hydroponic`, `hydroponic automation`

H AI: `AI hidroponik`, `AI farming`, `artificial intelligence hydroponics`, `predictive hydroponics`

I Purchase/price: `beli hidroponik`, `beli kit hidroponik`, `harga kit hidroponik`, `rekomendasi kit hidroponik`, `buy hydroponic kit`, `hydroponic kit price`

J Sustainability: `hidroponik berkelanjutan`, `media tanam ramah lingkungan`, `sustainable hydroponics`, `biodegradable growing media`

K Bagasse: `ampas tebu`, `limbah tebu`, `bagasse`, `sugarcane bagasse`, `bagasse growing media`, `bagasse hydroponics`

L Small space: `hidroponik lahan sempit`, `hidroponik balkon`, `hidroponik kos`, `urban gardening`, `small space hydroponics`

M Experience: `pengalaman hidroponik`, `kesalahan hidroponik pemula`, `hydroponic beginner mistakes`, `lessons learned hydroponics`

N Product/competitor: dynamically extract product and competitor names from collected content and expand queries.

## Query matrix
Generate `topic x problem x intent x language x geography x platform` combinations.

## Iterative expansion
After the first 500-1,000 records, extract slang, collocations, misspellings, product names, competitor names, and local terms. Add only high-signal terms. Track marginal yield of each query batch. Stop expanding when new queries produce little novel high-value content.

Keep an exclusion list for unrelated meanings and log every exclusion rule.
