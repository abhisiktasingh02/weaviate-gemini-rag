```markdown
# 🤖 Weaviate–Gemini RAG Bot (Production Architecture)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Weaviate](https://img.shields.io/badge/Weaviate-v4-green)
![RAG](https://img.shields.io/badge/RAG-Production--Grade-purple)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange)

A **production-grade Retrieval-Augmented Generation (RAG)** system that allows you to chat with PDF documents using **Weaviate vector search** and **Google Gemini LLMs**.

This project is designed with **clean architecture, modular components, hallucination guardrails, and multimodal ingestion**, demonstrating how RAG systems are built in real-world AI applications.

---

## 🚀 What This Project Demonstrates

✔ End-to-end RAG pipeline  
✔ Multimodal ingestion (text, tables, images + OCR)  
✔ LLM-based query intent parsing  
✔ Vector search with relevance guardrails  
✔ Clean separation of retrieval & generation  
✔ Scalable, extensible architecture  

This is **not a tutorial repo** — it reflects **production engineering practices**.

---

## ✨ Key Features

### 📄 Multimodal PDF Ingestion
- Text extraction from PDFs
- Table extraction using `pdfplumber`
- OCR on images using `pytesseract`
- Token-aware chunking with overlap

### 🧠 Intelligent Query Parsing
- Uses Gemini to extract:
  - Search intent (definition, explanation, summary, etc.)
  - Semantic search query
  - Modality filters (text / table / image)

### 🔍 Vector Retrieval with Guardrails
- Semantic search via Weaviate
- Distance-based relevance filtering
- Out-of-scope query rejection to reduce hallucinations

### ✍️ Grounded Answer Generation
- LLM answers strictly constrained to retrieved context
- Explicit grounding rules to prevent external knowledge leakage

---

## 🏗️ System Architecture


User Query
    ↓
LLM Query Parser
    ↓
Vector Retrieval (Weaviate)
    ↓
Relevance Guardrails
    ↓
Context-Grounded Answer Generation (Gemini)
    ↓
Final Response + Source Pages

---

## 🛠️ Prerequisites

Before running the project, ensure you have:

- **Docker & Docker Compose**
- **Python 3.10+**
- **Google API Key (Gemini access)**
- **Tesseract OCR**
- **Poppler (PDF utilities)**

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/abhisiktasingh02/weaviate-gemini-rag.git
cd weaviate-gemini-rag
````

---

### 2️⃣ Create `.env` File

```ini
GOOGLE_API_KEY=your_google_api_key
GOOGLE_PROJECT_ID=your_google_project_id
LLM_MODEL=gemini-2.5-flash
```

---

### 3️⃣ Start Weaviate (Docker)

```bash
docker-compose up -d
```

Verify:

```bash
docker ps
```

---

### 4️⃣ Python Environment Setup

#### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If OCR fails, ensure **Tesseract** and **Poppler** are installed and added to PATH.

---

## ▶️ Running the Application

From the **project root**:

```bash
python -m app.main
```

---

### Expected Flow

```text
Enter the path to the PDF document:
Apples_Product_Use_Electricity_Strategy.pdf

✅ Document ingestion completed.

🤖 Hi I'm Weaviate Bot. Ask me anything related to the doc! Type 'bye' to quit
```

---

### Example Queries

**In-scope**

```
Summarize Apple’s electricity strategy
```

**Out-of-scope**

```
Who is the CEO of Microsoft?
```

---

## 📁 Project Structure

```text
weaviate-gemini-rag/
├── app/
│   ├── main.py                # Application entry point
│   ├── config/                # Environment & prompt configs
│   ├── ingestion/             # PDF text, table, image ingestion
│   ├── query/                 # LLM-based query parsing & filters
│   ├── retrieval/             # Vector search logic
│   ├── generation/            # Grounded answer generation
│   ├── guardrails/            # Relevance & hallucination checks
│   ├── db/                    # Weaviate schema & client setup
│   └── utils/                 # Shared helpers
│
├── docker-compose.yml
├── requirements.txt
├── .env                       # Ignored by git
└── README.md
```

---

## 🧠 Design Decisions

* **Single-pass retrieval** ensures guardrails and generation use identical context
* **Explicit grounding rules** prevent hallucinations
* **Schema idempotency** avoids accidental data loss
* **Modular architecture** supports future extensions (FastAPI, hybrid search, eval)

---

## 🧩 Planned Enhancements

* Hybrid search (BM25 + vector)
* RAG evaluation metrics (faithfulness, recall)
* FastAPI service layer
* Multi-PDF memory & chat history
* Observability & tracing

---

## 🤝 Contributing

Contributions, ideas, and reviews are welcome.
Feel free to open an issue or submit a PR.

---

## 📌 Author

**Abhisikta Singh**
Software Engineer | AI Systems | RAG & LLM Engineering
[LinkedIn](https://www.linkedin.com/in/abhisiktasingh/)

```