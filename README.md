# AI Instagram Müştəri Tapan & Analiz Paneli

Süni intellekt (Gemini AI) dəstəkli Instagram müştəri tapan, analiz edən və fərdiləşdirilmiş mesajlar hazırlayan veb platforması.

## 🚀 Xüsusiyyətlər
- **Ağıllı Axtarış**: Açar sözlər üzrə Instagram profillərinin aşkarlanması və analizi.
- **AI Mesaj Generatoru**: Tapılmış bizneslər üçün fərdiləşdirilmiş təklif və müraciət mesajlarının yaradılması.
- **İdarəetmə Paneli**: FastAPI və sadə interfeys ilə vizual nəticələr və status izləmə.
- **Təhlükəsizlik**: API açarları kodda deyil, .env mühit dəyişənlərində saxlanılır.

## 🛠️ Quraşdırma

1. **Kitabxanaları quraşdırın:**
   `ash
   pip install -r requirements.txt
   `

2. **Mühit dəyişənlərini təyin edin:**
   - .env.example faylının surətini çıxarıb adını .env edin:
     `ash
     cp .env.example .env
     `
   - .env faylını açıb öz GEMINI_API_KEY açarınızı daxil edin:
     `env
     GEMINI_API_KEY=your_gemini_api_key_here
     `

3. **Tətbiqi başladın:**
   `ash
   python server.py
   # və ya Windows-da:
   start.bat
   `
   Brauzerinizdə http://localhost:8000 ünvanına daxil olun.
