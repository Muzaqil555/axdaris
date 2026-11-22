# AI Instagram Müştəri Tapan & Analiz Paneli

Gemini AI ilə işləyən veb panel: verilən sahə və şəhər üzrə Instagram biznes profillərini tapır, hər biznes üçün ən çox gəlir gətirəcək avtomatlaşdırma sistemini seçir və ona uyğun fərdi satış mesajı (Azərbaycan dilində) hazırlayır.

## 🚀 Xüsusiyyətlər

- **Müştəri axtarışı:** sahə (məs. "gözəllik salonu") və şəhər (məs. "Bakı") üzrə Instagram biznes profillərinin siyahısı.
- **AI analiz:** hər biznes üçün ən uyğun sistem (rezervasiya botu, WhatsApp satış hunisi, loyallıq avtomatlaşdırması və s.), seçimin səbəbi və aylıq əlavə gəlir təxmini.
- **Fərdi mesaj:** biznesin adına və sahəsinə uyğun qısa Instagram DM mətni.
- **Panel və eksport:** nəticələr SQLite bazasında saxlanır, brauzerdə göstərilir və `output/leads.csv` faylına çıxarılır.
- **Təkrar yoxdur:** eyni profil iki dəfə saxlanmır, artıq analiz olunmuş profil yenidən AI-ya göndərilmir.

> **Diqqət:** profillər veb-scraping ilə deyil, Gemini-nin biliyindən gəlir. AI bəzən mövcud olmayan və ya köhnəlmiş hesab təklif edə bilər. Mesaj göndərməzdən əvvəl hər profili yoxlayın.

## 🛠️ Quraşdırma

1. **Kitabxanaları quraşdırın:**

   ```bash
   pip install -r requirements.txt
   ```

2. **API açarını təyin edin.** `.env.example` faylının surətini `.env` adı ilə çıxarın və öz açarınızı yazın ([Google AI Studio](https://aistudio.google.com/apikey)-dan pulsuz alına bilər):

   ```bash
   cp .env.example .env
   ```

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Açar yoxdursa, tətbiq sınaq (mock) məlumatları ilə işləyir.

## ▶️ İşə salmaq

**Veb panel:**

```bash
python -m uvicorn server:app --port 8000
```

Sonra brauzerdə <http://localhost:8000> ünvanını açın. Windows-da `start.bat` faylına iki dəfə klikləmək kifayətdir: server başlayır və brauzer özü açılır.

**Komanda sətri (CLI):**

```bash
python main.py
```

Sahəni, şəhəri və sınaq rejimini soruşur, nəticəni `output/leads.csv`-yə yazır.

## 🧪 Testlər

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Testlər sınaq məlumatları və saxta AI ilə işləyir, API açarı tələb etmir.

## 📁 Struktur

| Fayl | Vəzifəsi |
|---|---|
| `server.py` | FastAPI server və veb panelin API-si |
| `main.py` | Komanda sətri versiyası |
| `app/pipeline.py` | Axtarış → təmizləmə → saxlama → AI → CSV axını |
| `app/scraper.py` | Gemini ilə profil axtarışı |
| `app/ai_generator.py` | Sistem seçimi və satış mesajı |
| `app/database.py` | SQLite bazası və CSV eksportu |
| `static/` | Veb panelin HTML, CSS və JS faylları |

## 🔒 Təhlükəsizlik

API açarı kodda deyil, `.env` faylında saxlanır və `.gitignore` sayəsində GitHub-a düşmür.
