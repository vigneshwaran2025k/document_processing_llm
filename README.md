# 📄 Document Processing with LLM & OCR 🚀  
Extract structured data from PDFs, images (JPG/PNG), CSVs, and Excel files using **OCR & AI-powered LLM processing**.

## 📌 Features  
✅ **Supports Multiple File Formats**: CSV, XLSX, PDF, JPG, PNG  
✅ **OCR for Image & PDF Processing**: Extracts text using **Tesseract OCR**  
✅ **AI-Powered JSON Extraction**: Uses **LLM (Large Language Model)** to structure extracted text into JSON  
✅ **Handles Large Documents**: Supports multi-page PDFs and structured tabular data  
✅ **FastAPI Backend**: Lightweight & efficient API with error handling  

---

## 🛠️ Tech Stack  
- **FastAPI** 🚀 (Backend framework)  
- **Tesseract OCR** 🔍 (Image text extraction)  
- **PyMuPDF (Fitz)** 📄 (PDF text processing)  
- **Pandas** 📊 (CSV/XLSX handling)  
- **Python** 🐍 (Core language)  
- **LLM (Language Model)** 🤖 (For structured JSON extraction)  

---

## 🔧 Installation Guide  
## install this 
Tesseract 
```sh
https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe
```


### 1️⃣ Install Dependencies  
Make sure you have **Python 3.12** installed.  

```sh
pip install -r requirements.txt
```
### RUN command
```sh
uvicorn main:app --reload
```


