import streamlit as st
import json
import re
import os
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Toraja Translate AI",
    page_icon="🏡",
    layout="centered",
)

# ── Custom CSS — Warm earthy Toraja aesthetic ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap');

*, html, body { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

/* Background — warm terracotta earthy */
.stApp {
    background: #1a0e08;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(139,69,19,0.25) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(184,115,51,0.15) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 50%, rgba(26,14,8,1) 0%, transparent 100%);
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
        rgba(184,115,51,0.03) 40px,
        rgba(184,115,51,0.03) 41px
    ),
    repeating-linear-gradient(
        -45deg,
        transparent,
        transparent 40px,
        rgba(184,115,51,0.03) 40px,
        rgba(184,115,51,0.03) 41px
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
    color: #f5deb3;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}
.hero h1 span { color: #cd853f; font-style: italic; }
.hero-sub {
    color: #9e7e5a;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-weight: 300;
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
    color: #9e7e5a;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

/* ── Input area ── */
.stTextArea textarea {
    background: rgba(205,133,63,0.08) !important;
    border: 1px solid rgba(205,133,63,0.25) !important;
    border-radius: 12px !important;
    color: #f5deb3 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(205,133,63,0.6) !important;
    box-shadow: 0 0 0 3px rgba(205,133,63,0.1) !important;
}
.stTextArea textarea::placeholder { color: #6b5040 !important; }

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
    box-shadow: 0 8px 24px rgba(139,69,19,0.4) !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
    background: rgba(205,133,63,0.08) !important;
    border: 1px solid rgba(205,133,63,0.25) !important;
    border-radius: 10px !important;
    color: #f5deb3 !important;
}
label, .stTextArea label, .stSelectbox label {
    color: #9e7e5a !important;
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
    background: rgba(205,133,63,0.07);
    border: 1px solid rgba(205,133,63,0.2);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin: 0.75rem 0;
    position: relative;
    overflow: hidden;
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
    color: #cd853f;
    margin-bottom: 0.75rem;
}
.translation-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    line-height: 1.6;
    color: #f5deb3;
    font-weight: 600;
}
.original-text {
    font-size: 0.95rem;
    color: #b8936a;
    line-height: 1.7;
    font-style: italic;
}
.context-text {
    font-size: 0.9rem;
    color: #c8a882;
    line-height: 1.8;
}
.word-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 0.5rem;
}
.word-item {
    background: rgba(139,69,19,0.2);
    border: 1px solid rgba(205,133,63,0.2);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
}
.word-toraja {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f5deb3;
}
.word-indo {
    font-size: 0.8rem;
    color: #9e7e5a;
    margin-top: 2px;
}
.cultural-badge {
    display: inline-block;
    background: rgba(139,69,19,0.3);
    border: 1px solid rgba(205,133,63,0.35);
    color: #e8c49a;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 3px 3px 3px 0;
    letter-spacing: 0.5px;
}

/* ── Examples row ── */
.example-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 0.5rem;
}
.chip {
    background: rgba(205,133,63,0.1);
    border: 1px solid rgba(205,133,63,0.2);
    color: #b8936a;
    padding: 5px 12px;
    border-radius: 99px;
    font-size: 0.8rem;
    cursor: pointer;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #4a3020;
    font-size: 0.78rem;
    letter-spacing: 0.5px;
}
.stSpinner > div { border-top-color: #cd853f !important; }
hr { border-color: rgba(205,133,63,0.1) !important; margin: 1.2rem 0 !important; }
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

    system_prompt = f"""Kamu adalah ahli bahasa Toraja (Tae' dan Sa'dan Toraja) asli dari Tana Toraja, Sulawesi Selatan, Indonesia.

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

# Hero
st.markdown("""
<div class="hero">
  <span class="hero-ornament">🏡</span>
  <h1>Toraja<span>Translate</span></h1>
  <p class="hero-sub">Penerjemah Bahasa Toraja · Berbasis AI</p>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# Arah terjemahan
direction = st.selectbox(
    "Arah terjemahan",
    options=["toraja_to_indo", "indo_to_toraja"],
    format_func=lambda x: "🗣️ Toraja → Bahasa Indonesia" if x == "toraja_to_indo" else "🗣️ Bahasa Indonesia → Toraja",
)

# Placeholder sesuai arah
if direction == "toraja_to_indo":
    placeholder = 'Contoh: "Umba ko lako?" atau "Tabe\', la\' pia-pia i\'"'
    label = "Masukkan teks Bahasa Toraja"
else:
    placeholder = 'Contoh: "Selamat datang di rumah kami" atau "Apa kabarmu hari ini?"'
    label = "Masukkan teks Bahasa Indonesia"

text_input = st.text_area(label, placeholder=placeholder, height=120)

# Contoh kalimat
st.markdown("""
<div style="margin: -0.5rem 0 1rem;">
<p style="font-size:0.72rem; color:#6b5040; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">Contoh kalimat:</p>
<div class="example-chips">
  <span class="chip">Umba ko lako?</span>
  <span class="chip">Tabe' la' kumande</span>
  <span class="chip">Rambu Solo'</span>
  <span class="chip">Tongkonan</span>
  <span class="chip">Ma'nene'</span>
</div>
</div>
""", unsafe_allow_html=True)

translate_btn = st.button("🔤 Terjemahkan")

# ── Result ────────────────────────────────────────────────────────────────────
if translate_btn:
    if not text_input.strip():
        st.warning("Masukkan teks yang ingin diterjemahkan dulu ya!")
    else:
        with st.spinner("AI sedang menerjemahkan dan menggali konteks budaya Toraja..."):
            try:
                result = translate_toraja(text_input.strip(), direction)

                terjemahan   = result.get("terjemahan", "")
                lafal        = result.get("lafal", "")
                konteks      = result.get("konteks_budaya", "")
                kata_kata    = result.get("kata_per_kata", [])
                info_budaya  = result.get("info_budaya", [])
                tingkat      = result.get("tingkat_kesulitan", "Umum")
                catatan      = result.get("catatan", "")

                st.markdown('<div class="result-wrap">', unsafe_allow_html=True)

                # Hasil terjemahan utama
                lafal_html = f'<div style="font-size:0.85rem; color:#9e7e5a; margin-top:6px; font-style:italic;">🔊 Lafal: {lafal}</div>' if lafal else ""
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  TorajaTranslate AI — Melestarikan Bahasa & Budaya Toraja, Sulawesi Selatan<br>
  Tugas Besar Kecerdasan Buatan 2026
</div>
""", unsafe_allow_html=True)
