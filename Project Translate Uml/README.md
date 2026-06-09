# 🏡 TorajaTranslate AI

Aplikasi penerjemah Bahasa Toraja ↔ Bahasa Indonesia berbasis AI, dilengkapi konteks budaya dan penjelasan kata per kata.

---

## Cara Menjalankan

### 1. Install library
```bash
pip install -r requirements.txt
```
atau jika pakai Python launcher:
```bash
py -m pip install -r requirements.txt
```

### 2. Set API Key Anthropic
**PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxx"
```
**CMD:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx
```

### 3. Jalankan
```bash
streamlit run app.py
```
atau:
```bash
py -m streamlit run app.py
```

Buka browser: http://localhost:8501

---

## Fitur

- 🔄 Terjemah dua arah: Toraja → Indonesia & Indonesia → Toraja
- 📖 Arti kata per kata
- 🏛️ Konteks budaya Toraja (Rambu Solo', Tongkonan, Aluk Todolo, dll)
- 💡 Fakta budaya yang relevan
- 🔊 Panduan lafal/pengucapan
- 📚 Label tingkat kesulitan bahasa

---

## Teknologi

| Komponen | Teknologi |
|---|---|
| UI & Server | Python + Streamlit |
| AI Engine | Anthropic Claude (claude-sonnet-4) |
| Pengetahuan Budaya | Built-in Claude knowledge + prompt engineering |

---

*Dibuat untuk Tugas Besar Kecerdasan Buatan 2026 — Melestarikan Bahasa Toraja, Sulawesi Selatan*
