import streamlit as st
import json
import re
import os
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Toraja Translate AI",

    layout="centered",
)

# ── Custom CSS — Warm earthy Toraja aesthetic ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap');

*, html, body { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

/* Background — krem hangat */
.stApp {
    background: linear-gradient(135deg, #f5e6d0 0%, #ede0cc 50%, #e8d5b7 100%);
    min-height: 100vh;
}

/* Toraja geometric pattern overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 40px,
        rgba(139,69,19,0.06) 40px,
        rgba(139,69,19,0.06) 41px
    ),
    repeating-linear-gradient(
        -45deg,
        transparent,
        transparent 40px,
        rgba(139,69,19,0.06) 40px,
        rgba(139,69,19,0.06) 41px
    );
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { position: relative; z-index: 1; padding-top: 1rem !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2rem 0 0.5rem;
    position: relative;
}
.hero-ornament {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    display: block;
    filter: sepia(0.3);
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #3d1a00;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}
.hero h1 span { color: #5a1f00; font-style: italic; }
.hero-sub {
    color: #3d1a00;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #cd853f, transparent);
    margin: 1rem auto;
}

/* ── Direction selector ── */
.direction-label {
    font-size: 0.75rem;
    color: #3d1a00;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

/* ── Input area ── */
.stTextArea textarea {
    background: rgba(255,248,240,0.8) !important;
    border: 1px solid rgba(139,69,19,0.3) !important;
    border-radius: 12px !important;
    color: #3d1f0a !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(139,69,19,0.6) !important;
    box-shadow: 0 0 0 3px rgba(205,133,63,0.15) !important;
}
.stTextArea textarea::placeholder { color: #b8936a !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #8b4513, #cd853f) !important;
    color: #fff8f0 !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(139,69,19,0.3) !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
    background: rgba(255,248,240,0.8) !important;
    border: 1px solid rgba(139,69,19,0.3) !important;
    border-radius: 10px !important;
    color: #3d1f0a !important;
}
label, .stTextArea label, .stSelectbox label {
    color: #3d1a00 !important;
    font-size: 0.8rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ── Result cards ── */
.result-wrap {
    animation: fadeUp 0.5s ease forwards;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}

.card {
    background: rgba(255,248,235,0.85);
    border: 1px solid rgba(139,69,19,0.2);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin: 0.75rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 16px rgba(139,69,19,0.1);
    backdrop-filter: blur(4px);
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #cd853f, #8b4513);
    border-radius: 3px 0 0 3px;
}
.card-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #5a1f00;
    margin-bottom: 0.75rem;
}
.translation-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    line-height: 1.6;
    color: #3d1f0a;
    font-weight: 600;
}
.original-text {
    font-size: 0.95rem;
    color: #3d1a00;
    line-height: 1.7;
    font-style: italic;
}
.context-text {
    font-size: 0.9rem;
    color: #2a0f00;
    line-height: 1.8;
}
.word-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 0.5rem;
}
.word-item {
    background: rgba(255,235,200,0.7);
    border: 1px solid rgba(139,69,19,0.2);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
}
.word-toraja {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #2a0f00;
}
.word-indo {
    font-size: 0.8rem;
    color: #3d1a00;
    margin-top: 2px;
}
.cultural-badge {
    display: inline-block;
    background: rgba(205,133,63,0.15);
    border: 1px solid rgba(139,69,19,0.25);
    color: #2a0f00;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 3px 3px 3px 0;
    letter-spacing: 0.5px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #3d1a00;
    font-size: 0.78rem;
    letter-spacing: 0.5px;
}
.stSpinner > div { border-top-color: #cd853f !important; }
hr { border-color: rgba(139,69,19,0.15) !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Anthropic client ──────────────────────────────────────────────────────────
# ── Kamus Bahasa Toraja (Tae') ────────────────────────────────────────────────
KAMUS_TORAJA = """
KAMUS KATA DASAR BAHASA TORAJA (SA'DAN TORAJA) - TERVERIFIKASI AKURAT:

=== SAPAAN & SALAM (TERVERIFIKASI) ===
salama' melambi' = selamat pagi
salama' = selamat
kaboro'ki tama = selamat datang
salama' rokko tondok = selamat datang ke kampung
kurre sumanga' = terima kasih
tabe' = permisi / maaf (kata sopan sebelum melakukan sesuatu)
tabe' la' kumande = permisi, saya mau makan
tabe' la' lako = permisi, saya mau pergi

=== PERCAKAPAN SEHARI-HARI (TERVERIFIKASI) ===
umba nakua kareba? = apa kabar?
kareba apa? = apa kabar?
umba tu banuammu? = di mana rumahmu?
umba ko lako? = mau ke mana kamu?
ma'kalo'ka = saya lapar
marakka'ka = saya lapar
male ku lako sikola = saya pergi ke sekolah
tulungina' la = tolong bantu saya
bantuaka = tolong bantu saya
iyo = iya / ya
tang = tidak / bukan

=== KATA TANYA ===
umba = ke mana
sanga = apa
pira = berapa
nani = di mana
yamo = siapa
mbani = di mana (posisi/lokasi)

=== KATA KERJA UMUM ===
kumande = makan
minum = minum
lako = pergi
mai = datang / kemari
tindo = tidur
bangun = bangun
masak = memasak
pangngala' = ambil
tama = masuk
pura = selesai / sudah
mo = sudah (akhiran)
la' = akan / mau (kata depan aksi)

=== KATA SIFAT ===
mapia = baik / bagus
kada = buruk / jelek
malasa = sakit
waras = sehat
buda = banyak
kodi' = sedikit
balao = besar
kodi = kecil
mapari = capek / lelah
masarro = susah / sulit
gampang = mudah

=== KATA BENDA SEHARI-HARI ===
banua = rumah
tongkonan = rumah adat Toraja
padang = sawah / ladang
bua' = buah
barre = nasi
ba'ba = pintu
dena = adik
londong = ayam jantan
tedong = kerbau (hewan penting dalam budaya Toraja)
sapan = jembatan

=== BUDAYA & RITUAL ===
rambu solo' = upacara pemakaman / adat kematian Toraja
rambu tuka' = upacara syukuran / adat kehidupan (pernikahan, panen, dll)
aluk todolo = kepercayaan leluhur / agama tradisional Toraja
ma'nene' = ritual membersihkan dan mengganti pakaian jenazah leluhur
to minaa = pemimpin ritual adat Toraja
puya = alam baka / surga dalam kepercayaan Toraja
tau-tau = patung kayu menyerupai almarhum
liang = makam batu Toraja
pa'piong = masakan daging dalam bambu khas Toraja

=== ANGKA ===
mesa = satu
dua = dua
tallu = tiga
appa' = empat
lima = lima
ennem = enam
pitu = tujuh
karua = delapan
kasera = sembilan
sampulo = sepuluh

=== WAKTU ===
bongi = malam
allo = siang / hari
maingan = sekarang
tae'mo = sudah tidak ada
rao = besok
nangin = kemarin
melambi' = pagi

=== CONTOH KALIMAT LENGKAP (TERVERIFIKASI AKURAT) ===
"Salama' melambi'" = "Selamat pagi"
"Kaboro'ki tama" = "Selamat datang"
"Salama' rokko tondok" = "Selamat datang ke kampung"
"Kurre sumanga'" = "Terima kasih"
"Umba tu banuammu?" = "Di mana rumahmu?"
"Ma'kalo'ka" = "Saya lapar"
"Marakka'ka" = "Saya lapar"
"Umba nakua kareba?" = "Apa kabar?"
"Kareba apa?" = "Apa kabar?"
"Male ku lako sikola" = "Saya pergi ke sekolah"
"Tulungina' la" = "Tolong bantu saya"
"Bantuaka" = "Tolong bantu saya"
"Tabe' la' kumande" = "Permisi, saya mau makan"
"Umba ko lako?" = "Mau ke mana kamu?"

=== KAMUS PERCAKAPAN SEHARI-HARI (TERVERIFIKASI DARI SUMBER ASLI) ===
rokok = tole'
merokok = mattole'
sirih = pangngan
topi = songko'
mulut = puduk
kaki = lentek
tangan = lima
menurun = solo'
mendaki = tuka'
dingin = madingin
jangan = andi'
jangan pergi = andi' male
gagah = ga'gak
terus = tarru'
murah = mara / marawa
mahal = masuli'
berapa harganya = pira allinna
masuk = mentama
rambut = biluak
mata = mata
hidung = illing
jam berapa = tette' pira
permisi = paramisi / tabe'
nenek = nene' baine
kakek = nene' muane
pergi = male
datang = sae
tiba / sampai = rampo
kakak perempuan = kaka' baine
kakak laki-laki = kaka' muane
ibu = indo'
ayah = ambe'
air = wai
minum = mangngiru'
tidur = mamma'
dimana = umbanai
kemana = umba naolai
mengapa = matumbai
siapa = minda
dia = ia
saya = aku'
malas = masorro
kuat = mawatang
letih = bo'yo
dengan = sola
cepat = madomi'
semua = ianasang
boleh = ma'din
perempuan = baine / pia baine
mandi = mendio'
apa kabar = apa kareba
terima kasih kembali = kurre sumanga' duka
salam jumpa = salama' sitammu
dimana rumah kamu = umba nai banuanmu
siapa nama kamu = inda sangammu
selamat sore = salama' makaren
selamat malam = salama' mabongi
berdekatan = sikandappi
dekat = mandappi'
kapan = piran
jembatan = tete
jalan raya = batatta
sungai = salu
gunung = buntu
kampung = tondok
hari ini = allo totemo
jalan-jalan = sumalong

=== KAMUS LENGKAP BAHASA TORAJA (A-Z) ===
abu = abu
ada = den
adapun = ia tu
adik = adi
air = uai / wai
alir / mengalir = lolong
akan = la
akhir = tampak
Allah = Puang
ambil = ala / alai
anak = anak
anggur = anggoro'
asap = rambu
atap = papa
atas = do / dao
babi = bai
bagi = bagi
baik = melo
bagus = mellong
karena = saba' / belanna
bahasa = basa
bahtera = lopi
bahu = palempeng
bangkit = ke'de
bangsa = bangsa
bangun = millik
banyak = buda
barat = kalambunan
bening = malino
berangkat = male
berani = barani
berat = magasa
beri = ben
berkat = passakke
besar = kapua
besok = masiang
betina = birang
biji = lise'
bimbing = renden
cabang = tangke
cakrawala = batara
cari = daka'
cela = sayuan
celah = alla'
cerdik = matangngaran
cucu = ampo
cicit = ampo / uttu'
coklat = cokla
curang = kallassik
daging = duku'
dalam = lan
damai = marampa'
darah = rara
darat = karangkean
datar = marante
daun = daun
debu = barra-barra
dekat = kandappi'
delapan = karua
dengar = rangngi
derita = parri'
diam = kappa / marippi
dingin = ma'didik
diri = kale
berdiri = bendan
doa = sambayang
dosa = kasalan
dua = da'dua
duduk = no'ko'
duri = duri
emas = bulaan
empat = a'pa'
enam = annan
fajar = mata allo
firman = kada
gagah = maganta'
gembala = to manglaa
genap = ganna'
gila = maro
gua = lo'ko'
gulita = parrak
gunung = buntu
habis = tappu'
hadap = tingayo
hadir = den
hakim = to parengnge'
hamil = kia'nak / ma'tambuk
hapus = sapu
haram = pemali
harap = rannu
hari = allo
harta = barang
hasil = assele'
hembus = pamurru'
hendak = morai
henti = torro
hewan = patuoan
hidung = illong
hidup = tuo
hijau = maido
hilang = ta'de
hujan = uran / peuranan
hukum = atoran
ikut = turu'
imam = to minaa
ingin = morai
isi = issi
istirahat = melayo
istri = baine
jadi = dadi
jaga = jaga
jahat = kadake gau'
jalan = lalan
jalar = mendonglo'
janji = dandi / basse
jantan = londong
jatuh = tobang
jauh = mambela
jawab = balii
jelek = kadake
jernih = malino
juga = duka
jumpai = tammui
kabut = ambun
kacau = maritu
kakek = nene' muane
kalah = talo
kambing = beke
kapan = piran
karunia = pa'kamasean
kasih = ben
kata = kada
kaya = sugi'
ikan = bale
kayu = kayu
kecewa = mallo
kecil = bitti'
kejar = ula'
kekal = tontong sae lakona
kelakuan = gau'
keledai = donga
kenal = tandai
keluar = tassu'
keluh = sarro
kembali = sule
kemarau = pealloan
kepala = kapala
kumpul = rampun
lahir = dadi
laki-laki = muane
laku = gau' / malaku
lalu = anna
lama = masai
lambat = mela'
langit = langi'
langkah = tengka
larang = gagai
lari = ma'dondo
lapar = tang dia'
laut = tasik
lawan = uali
mabuk = malango
main = maningo
makan = kumande
malam = bongi
malu = sirik
mana = umba
manusia = tau
marah = sengke
masa = attu
mau = morai
matahari = mata allo
mati = mate
melata = mendonglo'
menang = patalo
menantu = mamintu
meninggal = mate
merpati = bu'ku'
nama = sanga
negeri = tondok
nyawa = deata / sumanga'
pikir = tangnga'
pilih = pili
pindah = mellele
pintu = ba'ba
pisah = sarak
sahabat laki-laki = sangmane
sahabat perempuan = sangbaine
pacar = rendeng
padang = padang
pagi = melambi'
pakaian = bayu
panah = pana
pohon = garontok kayu
patah = le'to
sahut = mebali
sakit = masaki
puji = pudi
pulang = sule
panas = malassu
panggil = tambai
panjang = kalando / lambe'
pasar = pasa'
pedang = pa'dang
raja = datu
salam = salama'
satu = misa'
saudara = siulu'
sayang = rendeng
sebab = belanna
sedih = tumangi'
segala = mintu'
selesai = nangka / mangka
semua = mintu' / nasang
seperti = susi
sepuluh = sang pulo
seratus = saratu'
siang = masiang / allo
suara = gamara
sungguh = tonganna
susah = masussa
syukur = kurre sumanga'
tabur = ambo'
tengah = tangnga
tepung = ta'pung
terang = tarrang
terbang = mettia'
tetap = tontong
tiang = patongkon
tidur = mamma'
tiga = tallu
tinggi = madoo / malangka'
tipu = pakena
tahu = tandai
tahun = taun
takut = mataku'
taman = pa'lak
tanah = padang
tarik = tare'
telanjang = kanderang
tempat = inan
tua = matua
tuan = puang
tujuh = pitu
tumbuh = tuo
tunggu = kampa
tunjuk = dullu
turun = mengkalao
tubuh = kale
tutup = tutu'
uang = seng
ular = ula'
umur = muru'
upah = saro
wajah = lindo
waktu = attu
"""

def translate_toraja(text: str, direction: str) -> dict:
    api_key = os.environ.get("GROQ_API_KEY", "")

    if direction == "toraja_to_indo":
        src_lang = "Bahasa Toraja (Tae' / Sa'dan Toraja)"
        tgt_lang = "Bahasa Indonesia"
        src_label = "Toraja"
        tgt_label = "Indonesia"
    else:
        src_lang = "Bahasa Indonesia"
        tgt_lang = "Bahasa Toraja (Tae' / Sa'dan Toraja)"
        src_label = "Indonesia"
        tgt_label = "Toraja"

    system_prompt = f"""Kamu adalah ahli bahasa Toraja (Tae' dan Sa'dan Toraja) asli dari Toraja Utara, Sulawesi Selatan, Indonesia.

PENTING: Gunakan kamus referensi berikut sebagai acuan utama terjemahan. Kamus ini HARUS diikuti dengan tepat:

{KAMUS_TORAJA}

ATURAN TERJEMAHAN:
1. Selalu gunakan kamus di atas sebagai referensi utama
2. Jika kata ada di kamus, WAJIB gunakan terjemahan dari kamus tersebut
3. Tabe' la' kumande = "Permisi, saya mau makan" (BUKAN selamat datang)
4. Umba ko lako = "Mau ke mana kamu?" 
5. Mbani = "di mana" (untuk menanyakan lokasi/posisi)
6. Untuk kata yang tidak ada di kamus, terjemahkan berdasarkan pengetahuan bahasa Toraja
7. Perhatikan konteks budaya Toraja dalam setiap terjemahan

Selalu respond dengan format JSON yang valid saja. Jangan tambahkan teks apapun di luar JSON."""

    prompt = f"""Terjemahkan teks berikut dari {src_lang} ke {tgt_lang}:

TEKS: "{text}"

Berikan response dalam format JSON berikut:
{{
  "teks_asli": "{text}",
  "terjemahan": "<hasil terjemahan lengkap dan akurat berdasarkan kamus>",
  "lafal": "<cara membaca/pengucapan jika ada yang unik, atau kosong jika tidak ada>",
  "konteks_budaya": "<penjelasan konteks budaya Toraja yang relevan, 2-3 kalimat>",
  "kata_per_kata": [
    {{"toraja": "<kata toraja>", "indonesia": "<arti kata dari kamus>"}},
    {{"toraja": "<kata toraja>", "indonesia": "<arti kata dari kamus>"}}
  ],
  "info_budaya": ["<fakta budaya 1>", "<fakta budaya 2>", "<fakta budaya 3>"],
  "tingkat_kesulitan": "<Umum/Dialek Khusus/Ritual/Sastra>",
  "catatan": "<catatan tambahan jika ada variasi dialek atau penggunaan khusus, bisa kosong>"
}}

Catatan: untuk kata_per_kata, isi dengan pasangan kata dari teks asli.
Untuk {src_label} ke {tgt_label}."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1500,
        "temperature": 0.3,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

# ── UI ─────────────────────────────────────────────────────────────────────────

# ── Kuis data (dari kamus terverifikasi) ─────────────────────────────────────
KUIS_DATA = [
    # Sapaan & Salam
    {"toraja": "Kurre sumanga'", "indonesia": "Terima kasih", "pilihan": ["Selamat datang", "Terima kasih", "Permisi", "Selamat pagi"]},
    {"toraja": "Salama' melambi'", "indonesia": "Selamat pagi", "pilihan": ["Selamat malam", "Selamat sore", "Selamat pagi", "Selamat datang"]},
    {"toraja": "Salama' mabongi", "indonesia": "Selamat malam", "pilihan": ["Selamat pagi", "Selamat malam", "Selamat sore", "Selamat datang"]},
    {"toraja": "Salama' makaren", "indonesia": "Selamat sore", "pilihan": ["Selamat pagi", "Selamat malam", "Selamat sore", "Terima kasih"]},
    {"toraja": "Kaboro'ki tama", "indonesia": "Selamat datang", "pilihan": ["Selamat tinggal", "Selamat datang", "Terima kasih", "Permisi"]},
    {"toraja": "Salama' sitammu", "indonesia": "Salam jumpa", "pilihan": ["Salam perpisahan", "Salam jumpa", "Selamat datang", "Terima kasih"]},
    {"toraja": "Tabe'", "indonesia": "Permisi / Maaf", "pilihan": ["Terima kasih", "Permisi / Maaf", "Selamat", "Tolong"]},
    {"toraja": "Iyo", "indonesia": "Iya / Ya", "pilihan": ["Tidak", "Iya / Ya", "Mungkin", "Belum"]},
    {"toraja": "Tang", "indonesia": "Tidak / Bukan", "pilihan": ["Iya", "Tidak / Bukan", "Mungkin", "Sudah"]},
    # Kata tanya
    {"toraja": "Umba ko lako?", "indonesia": "Mau ke mana kamu?", "pilihan": ["Siapa namamu?", "Di mana rumahmu?", "Mau ke mana kamu?", "Apa kabar?"]},
    {"toraja": "Apa kareba?", "indonesia": "Apa kabar?", "pilihan": ["Mau ke mana?", "Apa kabar?", "Siapa namamu?", "Di mana kamu?"]},
    {"toraja": "Umba tu banuammu?", "indonesia": "Di mana rumahmu?", "pilihan": ["Siapa namamu?", "Mau ke mana?", "Di mana rumahmu?", "Apa kabar?"]},
    {"toraja": "Inda sangammu?", "indonesia": "Siapa namamu?", "pilihan": ["Di mana rumahmu?", "Siapa namamu?", "Berapa harganya?", "Mau ke mana?"]},
    {"toraja": "Pira allinna?", "indonesia": "Berapa harganya?", "pilihan": ["Kapan datang?", "Berapa harganya?", "Di mana?", "Siapa?"]},
    {"toraja": "Piran?", "indonesia": "Kapan?", "pilihan": ["Di mana?", "Siapa?", "Kapan?", "Berapa?"]},
    {"toraja": "Minda?", "indonesia": "Siapa?", "pilihan": ["Siapa?", "Di mana?", "Kapan?", "Berapa?"]},
    {"toraja": "Matumbai?", "indonesia": "Mengapa?", "pilihan": ["Kapan?", "Di mana?", "Mengapa?", "Bagaimana?"]},
    # Kata kerja
    {"toraja": "Kumande", "indonesia": "Makan", "pilihan": ["Minum", "Tidur", "Makan", "Pergi"]},
    {"toraja": "Mamma'", "indonesia": "Tidur", "pilihan": ["Tidur", "Makan", "Duduk", "Berdiri"]},
    {"toraja": "Male", "indonesia": "Pergi", "pilihan": ["Datang", "Pergi", "Tidur", "Makan"]},
    {"toraja": "Sae", "indonesia": "Datang", "pilihan": ["Pergi", "Datang", "Pulang", "Tidur"]},
    {"toraja": "Sule", "indonesia": "Pulang / Kembali", "pilihan": ["Pergi", "Datang", "Pulang / Kembali", "Tidur"]},
    {"toraja": "Mangngiru'", "indonesia": "Minum", "pilihan": ["Makan", "Minum", "Tidur", "Pergi"]},
    {"toraja": "Mendio'", "indonesia": "Mandi", "pilihan": ["Tidur", "Makan", "Mandi", "Pergi"]},
    {"toraja": "Tiro", "indonesia": "Lihat", "pilihan": ["Dengar", "Lihat", "Bicara", "Jalan"]},
    {"toraja": "No'ko'", "indonesia": "Duduk", "pilihan": ["Berdiri", "Duduk", "Pergi", "Tidur"]},
    {"toraja": "Millik", "indonesia": "Bangun", "pilihan": ["Tidur", "Bangun", "Duduk", "Pergi"]},
    {"toraja": "Madomi'", "indonesia": "Cepat", "pilihan": ["Lambat", "Cepat", "Jauh", "Dekat"]},
    # Kata sifat
    {"toraja": "Mapia", "indonesia": "Baik / Bagus", "pilihan": ["Jelek", "Baik / Bagus", "Buruk", "Mahal"]},
    {"toraja": "Buda", "indonesia": "Banyak", "pilihan": ["Sedikit", "Besar", "Banyak", "Kecil"]},
    {"toraja": "Mambela", "indonesia": "Jauh", "pilihan": ["Dekat", "Jauh", "Tinggi", "Rendah"]},
    {"toraja": "Mandappi'", "indonesia": "Dekat", "pilihan": ["Jauh", "Dekat", "Tinggi", "Rendah"]},
    {"toraja": "Malassu", "indonesia": "Panas", "pilihan": ["Dingin", "Panas", "Hangat", "Sejuk"]},
    {"toraja": "Madingin", "indonesia": "Dingin", "pilihan": ["Panas", "Dingin", "Hangat", "Sejuk"]},
    {"toraja": "Masuli'", "indonesia": "Mahal", "pilihan": ["Murah", "Mahal", "Gratis", "Diskon"]},
    {"toraja": "Marawa", "indonesia": "Murah", "pilihan": ["Mahal", "Murah", "Gratis", "Bayar"]},
    {"toraja": "Mawatang", "indonesia": "Kuat", "pilihan": ["Lemah", "Kuat", "Sakit", "Capek"]},
    {"toraja": "Masorro", "indonesia": "Malas", "pilihan": ["Rajin", "Malas", "Cepat", "Lambat"]},
    {"toraja": "Bitti'", "indonesia": "Kecil", "pilihan": ["Besar", "Kecil", "Panjang", "Pendek"]},
    {"toraja": "Kapua", "indonesia": "Besar", "pilihan": ["Kecil", "Besar", "Panjang", "Pendek"]},
    # Kata benda - keluarga
    {"toraja": "Indo'", "indonesia": "Ibu", "pilihan": ["Ayah", "Kakak", "Ibu", "Adik"]},
    {"toraja": "Ambe'", "indonesia": "Ayah", "pilihan": ["Ibu", "Ayah", "Nenek", "Kakek"]},
    {"toraja": "Nene' baine", "indonesia": "Nenek", "pilihan": ["Kakek", "Nenek", "Bibi", "Paman"]},
    {"toraja": "Nene' muane", "indonesia": "Kakek", "pilihan": ["Nenek", "Kakek", "Bibi", "Paman"]},
    {"toraja": "Kaka' baine", "indonesia": "Kakak perempuan", "pilihan": ["Kakak laki-laki", "Adik perempuan", "Kakak perempuan", "Ibu"]},
    {"toraja": "Kaka' muane", "indonesia": "Kakak laki-laki", "pilihan": ["Kakak perempuan", "Kakak laki-laki", "Ayah", "Adik laki-laki"]},
    # Kata benda - tempat & alam
    {"toraja": "Banua", "indonesia": "Rumah", "pilihan": ["Sekolah", "Rumah", "Pasar", "Jalan"]},
    {"toraja": "Tondok", "indonesia": "Kampung / Desa", "pilihan": ["Kota", "Kampung / Desa", "Pasar", "Sekolah"]},
    {"toraja": "Tongkonan", "indonesia": "Rumah adat Toraja", "pilihan": ["Rumah biasa", "Rumah adat Toraja", "Istana", "Masjid"]},
    {"toraja": "Salu", "indonesia": "Sungai", "pilihan": ["Laut", "Danau", "Sungai", "Gunung"]},
    {"toraja": "Buntu", "indonesia": "Gunung", "pilihan": ["Laut", "Sungai", "Gunung", "Danau"]},
    {"toraja": "Tasik", "indonesia": "Laut", "pilihan": ["Sungai", "Danau", "Gunung", "Laut"]},
    {"toraja": "Tete", "indonesia": "Jembatan", "pilihan": ["Jalan", "Jembatan", "Sungai", "Gunung"]},
    {"toraja": "Pasa'", "indonesia": "Pasar", "pilihan": ["Sekolah", "Rumah", "Pasar", "Kantor"]},
    {"toraja": "Batatta", "indonesia": "Jalan raya", "pilihan": ["Jembatan", "Jalan raya", "Sungai", "Gunung"]},
    # Kata benda - hewan & alam
    {"toraja": "Tedong", "indonesia": "Kerbau", "pilihan": ["Sapi", "Kerbau", "Kambing", "Ayam"]},
    {"toraja": "Londong", "indonesia": "Ayam jantan", "pilihan": ["Ayam betina", "Bebek", "Ayam jantan", "Burung"]},
    {"toraja": "Beke", "indonesia": "Kambing", "pilihan": ["Sapi", "Kambing", "Kerbau", "Ayam"]},
    {"toraja": "Bale", "indonesia": "Ikan", "pilihan": ["Ayam", "Ikan", "Daging", "Telur"]},
    {"toraja": "Wai", "indonesia": "Air", "pilihan": ["Api", "Tanah", "Air", "Angin"]},
    {"toraja": "Riu", "indonesia": "Rumput", "pilihan": ["Pohon", "Bunga", "Rumput", "Daun"]},
    # Waktu
    {"toraja": "Bongi", "indonesia": "Malam", "pilihan": ["Pagi", "Siang", "Sore", "Malam"]},
    {"toraja": "Melambi'", "indonesia": "Pagi", "pilihan": ["Pagi", "Siang", "Sore", "Malam"]},
    {"toraja": "Allo", "indonesia": "Siang / Hari", "pilihan": ["Malam", "Siang / Hari", "Pagi", "Sore"]},
    {"toraja": "Masiang", "indonesia": "Besok", "pilihan": ["Kemarin", "Hari ini", "Besok", "Minggu depan"]},
    {"toraja": "Allo totemo", "indonesia": "Hari ini", "pilihan": ["Kemarin", "Hari ini", "Besok", "Minggu depan"]},
    # Budaya Toraja
    {"toraja": "Rambu Solo'", "indonesia": "Upacara pemakaman Toraja", "pilihan": ["Upacara pernikahan", "Upacara pemakaman Toraja", "Upacara panen", "Upacara kelahiran"]},
    {"toraja": "Rambu Tuka'", "indonesia": "Upacara syukuran Toraja", "pilihan": ["Upacara pemakaman", "Upacara syukuran Toraja", "Upacara perang", "Upacara adat"]},
    {"toraja": "Ma'nene'", "indonesia": "Ritual membersihkan jenazah leluhur", "pilihan": ["Ritual pernikahan", "Ritual panen", "Ritual membersihkan jenazah leluhur", "Ritual kelahiran"]},
    {"toraja": "Aluk Todolo", "indonesia": "Kepercayaan leluhur Toraja", "pilihan": ["Bahasa Toraja", "Kepercayaan leluhur Toraja", "Tarian Toraja", "Masakan Toraja"]},
    {"toraja": "Tau-tau", "indonesia": "Patung kayu menyerupai almarhum", "pilihan": ["Patung dewa", "Patung kayu menyerupai almarhum", "Patung raja", "Patung binatang"]},
    {"toraja": "Liang", "indonesia": "Makam batu Toraja", "pilihan": ["Rumah adat", "Makam batu Toraja", "Tempat ibadah", "Istana raja"]},
    {"toraja": "Pa'piong", "indonesia": "Masakan daging dalam bambu", "pilihan": ["Masakan ikan bakar", "Masakan daging dalam bambu", "Masakan nasi goreng", "Masakan sup"]},
    # Angka
    {"toraja": "Misa'", "indonesia": "Satu", "pilihan": ["Dua", "Tiga", "Satu", "Empat"]},
    {"toraja": "Da'dua", "indonesia": "Dua", "pilihan": ["Satu", "Dua", "Tiga", "Empat"]},
    {"toraja": "Tallu", "indonesia": "Tiga", "pilihan": ["Dua", "Tiga", "Empat", "Lima"]},
    {"toraja": "A'pa'", "indonesia": "Empat", "pilihan": ["Tiga", "Empat", "Lima", "Enam"]},
    {"toraja": "Lima", "indonesia": "Lima", "pilihan": ["Empat", "Lima", "Enam", "Tujuh"]},
    {"toraja": "Annan", "indonesia": "Enam", "pilihan": ["Lima", "Enam", "Tujuh", "Delapan"]},
    {"toraja": "Pitu", "indonesia": "Tujuh", "pilihan": ["Enam", "Tujuh", "Delapan", "Sembilan"]},
    {"toraja": "Karua", "indonesia": "Delapan", "pilihan": ["Tujuh", "Delapan", "Sembilan", "Sepuluh"]},
    {"toraja": "Kasera", "indonesia": "Sembilan", "pilihan": ["Delapan", "Sembilan", "Sepuluh", "Sebelas"]},
    {"toraja": "Sang pulo", "indonesia": "Sepuluh", "pilihan": ["Sembilan", "Sepuluh", "Sebelas", "Dua belas"]},
]

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-ornament">🛖</span>
  <h1>Toraja<span>Translate</span></h1>
  <p class="hero-sub">Melestarikan Bahasa & Budaya Toraja Utara</p>
  <div class="divider"></div>
  <p style="color:#3d1a00; font-size:0.82rem; font-style:italic; margin-top:-0.3rem;">
    ✦ Kurre Sumanga' — Toraja Utara ✦
  </p>
</div>
""", unsafe_allow_html=True)

# ── Tab navigasi ───────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔤 Terjemahkan", "🎯 Kuis Bahasa", "ℹ️ Tentang"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — TERJEMAHKAN
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    direction = st.selectbox(
        "Arah terjemahan",
        options=["toraja_to_indo", "indo_to_toraja"],
        format_func=lambda x: "🗣️ Toraja → Bahasa Indonesia" if x == "toraja_to_indo" else "🗣️ Bahasa Indonesia → Toraja",
    )

    if direction == "toraja_to_indo":
        label = "Masukkan teks Bahasa Toraja"
    else:
        label = "Masukkan teks Bahasa Indonesia"

    text_input = st.text_area(label, height=120)
    translate_btn = st.button("🔤 Terjemahkan")

    if translate_btn:
        if not text_input.strip():
            st.warning("Masukkan teks yang ingin diterjemahkan dulu ya!")
        else:
            with st.spinner("AI sedang menerjemahkan dan menggali konteks budaya Toraja..."):
                try:
                    result = translate_toraja(text_input.strip(), direction)

                    terjemahan  = result.get("terjemahan", "")
                    lafal       = result.get("lafal", "")
                    konteks     = result.get("konteks_budaya", "")
                    kata_kata   = result.get("kata_per_kata", [])
                    info_budaya = result.get("info_budaya", [])
                    tingkat     = result.get("tingkat_kesulitan", "Umum")
                    catatan     = result.get("catatan", "")

                    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)

                    # Hasil terjemahan + tombol salin
                    lafal_html = f'<div style="font-size:0.85rem; color:#3d1a00; margin-top:6px; font-style:italic;">🔊 Lafal: {lafal}</div>' if lafal else ""
                    st.markdown(f"""
                    <div class="card">
                      <div class="card-label">Hasil Terjemahan</div>
                      <div class="translation-text">{terjemahan}</div>
                      {lafal_html}
                      <div style="margin-top:10px;">
                        <span class="cultural-badge">📚 {tingkat}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Tombol salin
                    st.code(terjemahan, language=None)

                    # Teks asli
                    st.markdown(f"""
                    <div class="card">
                      <div class="card-label">Teks Asli</div>
                      <div class="original-text">"{text_input.strip()}"</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Kata per kata
                    if kata_kata:
                        words_html = ""
                        for w in kata_kata:
                            t = w.get("toraja", "")
                            i = w.get("indonesia", "")
                            if t and i:
                                words_html += f"""
                                <div class="word-item">
                                  <div class="word-toraja">{t}</div>
                                  <div class="word-indo">{i}</div>
                                </div>"""
                        if words_html:
                            st.markdown(f"""
                            <div class="card">
                              <div class="card-label">Arti Kata per Kata</div>
                              <div class="word-grid">{words_html}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    # Konteks budaya
                    if konteks:
                        st.markdown(f"""
                        <div class="card">
                          <div class="card-label">🏛️ Konteks Budaya Toraja</div>
                          <div class="context-text">{konteks}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Info budaya
                    if info_budaya:
                        badges = "".join(f'<span class="cultural-badge">✦ {i}</span>' for i in info_budaya)
                        st.markdown(f"""
                        <div class="card">
                          <div class="card-label">💡 Fakta Budaya</div>
                          <div style="margin-top:4px;">{badges}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Catatan
                    if catatan:
                        st.markdown(f"""
                        <div class="card" style="border-color:rgba(205,133,63,0.35);">
                          <div class="card-label">📝 Catatan</div>
                          <div class="context-text">{catatan}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("Terjemahan selesai! 🎉")

                except json.JSONDecodeError:
                    st.error("Format response AI tidak valid. Coba lagi ya!")
                except requests.exceptions.HTTPError as e:
                    st.error(f"Kesalahan API: {e}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — KUIS BAHASA TORAJA
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
      <div style="font-size:0.7rem; color:#5a1f00; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px;">Uji Kemampuanmu</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:#f5deb3; font-weight:600;">Kuis Bahasa Toraja</div>
      <div style="font-size:0.85rem; color:#3d1a00; margin-top:4px;">Tebak arti kata dalam Bahasa Toraja</div>
    </div>
    """, unsafe_allow_html=True)

    # Inisialisasi session state
    if "kuis_index" not in st.session_state:
        st.session_state.kuis_index = 0
        st.session_state.kuis_skor = 0
        st.session_state.kuis_jawab = None
        st.session_state.kuis_selesai = False
        import random
        st.session_state.kuis_urutan = random.sample(range(len(KUIS_DATA)), min(20, len(KUIS_DATA)))

    idx = st.session_state.kuis_index
    total = len(st.session_state.kuis_urutan)

    if st.session_state.kuis_selesai:
        skor = st.session_state.kuis_skor
        persen = int((skor / total) * 100)
        if persen >= 80:
            emoji = "🏆"
            pesan = "Luar biasa! Kamu sangat menguasai Bahasa Toraja!"
        elif persen >= 60:
            emoji = "⭐"
            pesan = "Bagus! Terus belajar Bahasa Toraja!"
        else:
            emoji = "📚"
            pesan = "Jangan menyerah! Terus berlatih ya!"

        st.markdown(f"""
        <div style="text-align:center; padding:2rem 0;">
          <div style="font-size:3rem;">{emoji}</div>
          <div style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#f5deb3; margin:0.5rem 0;">{skor} / {total}</div>
          <div style="font-size:1rem; color:#5a1f00; font-weight:600;">{persen}% Benar</div>
          <div style="font-size:0.9rem; color:#3d1a00; margin-top:0.5rem;">{pesan}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Mulai Kuis Lagi"):
            import random
            st.session_state.kuis_index = 0
            st.session_state.kuis_skor = 0
            st.session_state.kuis_jawab = None
            st.session_state.kuis_selesai = False
            st.session_state.kuis_urutan = random.sample(range(len(KUIS_DATA)), min(20, len(KUIS_DATA)))
            st.rerun()
    else:
        soal_idx = st.session_state.kuis_urutan[idx]
        soal = KUIS_DATA[soal_idx]

        # Progress bar
        progress = idx / total
        st.markdown(f"""
        <div style="margin: 0.5rem 0 1rem;">
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#3d1a00; margin-bottom:4px;">
            <span>Soal {idx + 1} dari {total}</span>
            <span>Skor: {st.session_state.kuis_skor}</span>
          </div>
          <div style="background:rgba(205,133,63,0.15); border-radius:99px; height:6px;">
            <div style="background:linear-gradient(90deg,#8b4513,#cd853f); border-radius:99px; height:6px; width:{int(progress*100)}%;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Soal
        st.markdown(f"""
        <div class="card" style="text-align:center; padding:2rem;">
          <div style="font-size:0.7rem; color:#5a1f00; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.75rem;">Apa artinya?</div>
          <div style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:#f5deb3; font-weight:700; font-style:italic;">"{soal['toraja']}"</div>
        </div>
        """, unsafe_allow_html=True)

        # Pilihan jawaban
        import random
        if "kuis_pilihan_acak" not in st.session_state or st.session_state.get("kuis_last_idx") != idx:
            acak = soal["pilihan"].copy()
            random.shuffle(acak)
            st.session_state.kuis_pilihan_acak = acak
            st.session_state.kuis_last_idx = idx

        pilihan = st.session_state.kuis_pilihan_acak
        jawaban = st.session_state.kuis_jawab

        col1, col2 = st.columns(2)
        for i, p in enumerate(pilihan):
            col = col1 if i % 2 == 0 else col2
            with col:
                if jawaban is None:
                    if st.button(p, key=f"jawab_{i}", use_container_width=True):
                        st.session_state.kuis_jawab = p
                        if p == soal["indonesia"]:
                            st.session_state.kuis_skor += 1
                        st.rerun()
                else:
                    if p == soal["indonesia"]:
                        st.success(f"✅ {p}")
                    elif p == jawaban:
                        st.error(f"❌ {p}")
                    else:
                        st.button(p, key=f"jawab_{i}", disabled=True, use_container_width=True)

        # Feedback & lanjut
        if jawaban is not None:
            if jawaban == soal["indonesia"]:
                st.markdown("""<div style="text-align:center; color:#4caf50; font-weight:600; margin:0.5rem 0;">🎉 Benar! Kurre sumanga'!</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="text-align:center; color:#f44336; font-weight:600; margin:0.5rem 0;">Jawaban benar: <span style="color:#5a1f00;">{soal['indonesia']}</span></div>""", unsafe_allow_html=True)

            if idx + 1 < total:
                if st.button("Soal Berikutnya →", use_container_width=True):
                    st.session_state.kuis_index += 1
                    st.session_state.kuis_jawab = None
                    if "kuis_pilihan_acak" in st.session_state:
                        del st.session_state.kuis_pilihan_acak
                    st.rerun()
            else:
                if st.button("Lihat Hasil Akhir 🏆", use_container_width=True):
                    st.session_state.kuis_selesai = True
                    st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — TENTANG
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div style="padding: 1rem 0;">
      <div class="card">
        <div class="card-label">🛖 Tentang Aplikasi</div>
        <div class="context-text">
          <b style="color:#5c2d0a;">TorajaTranslate AI</b> adalah aplikasi penerjemah Bahasa Toraja berbasis kecerdasan buatan yang dikembangkan untuk membantu melestarikan Bahasa dan Budaya Toraja Utara, Sulawesi Selatan, Indonesia.
          <br><br>
          Bahasa Toraja merupakan salah satu kekayaan budaya Indonesia yang perlu dijaga dan dilestarikan. Aplikasi ini hadir sebagai langkah kecil dalam mendokumentasikan dan memperkenalkan Bahasa Toraja kepada masyarakat luas.
        </div>
      </div>

      <div class="card">
        <div class="card-label">⚙️ Teknologi</div>
        <div class="context-text">
          <span class="cultural-badge">🐍 Python</span>
          <span class="cultural-badge">🎯 Streamlit</span>
          <span class="cultural-badge">🤖 Llama 3.3 70B</span>
          <span class="cultural-badge">⚡ Groq API</span>
          <span class="cultural-badge">📚 Kamus Toraja</span>
        </div>
      </div>

      <div class="card">
        <div class="card-label">✨ Fitur</div>
        <div class="context-text">
          <span class="cultural-badge">🔄 Terjemah 2 Arah</span>
          <span class="cultural-badge">📖 Arti Kata per Kata</span>
          <span class="cultural-badge">🏛️ Konteks Budaya</span>
          <span class="cultural-badge">💡 Fakta Budaya</span>
          <span class="cultural-badge">🎯 Kuis Bahasa</span>
          <span class="cultural-badge">📋 Salin Hasil</span>
        </div>
      </div>

      <div class="card">
        <div class="card-label">🌏 Tentang Bahasa Toraja</div>
        <div class="context-text">
          Bahasa Toraja atau Tae' adalah bahasa yang digunakan oleh Suku Toraja di Kabupaten Tana Toraja dan Toraja Utara, Sulawesi Selatan. Bahasa ini memiliki beberapa dialek, termasuk dialek Makale-Rantepao yang paling umum digunakan.
          <br><br>
          Budaya Toraja dikenal melalui upacara <b style="color:#8b4513;">Rambu Solo'</b> (pemakaman) dan <b style="color:#8b4513;">Rambu Tuka'</b> (syukuran), serta rumah adat <b style="color:#8b4513;">Tongkonan</b> yang ikonik.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
