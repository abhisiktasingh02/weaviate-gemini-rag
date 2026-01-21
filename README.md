Here is a professional, formatted `README.md` for your repository. It organizes your features, prerequisites, and setup instructions clearly for anyone visiting your project.

You can copy-paste the raw markdown code block below directly into your GitHub file.

---

```markdown
# 🤖 Weaviate-Gemini RAG Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Weaviate](https://img.shields.io/badge/Weaviate-v4-green)
![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange)

A powerful **Retrieval-Augmented Generation (RAG)** chatbot that allows you to "chat" with your PDF documents.

This project combines **Weaviate's** vector search capabilities with **Google Gemini's** generative AI to answer questions based strictly on document context. It features multimodal ingestion (text, tables, and images), intelligent query parsing, and strict scope checking to minimize AI hallucinations.

## ✨ Key Features

* **📄 Multimodal Ingestion:** Uses `pdfplumber` and `pytesseract` to extract text, tables, and perform OCR on images within PDFs.
* **🧠 Intelligent Query Parsing:** Leverages Gemini to pre-process user queries—extracting intent (lookup vs. explanation) and keywords before searching.
* **🔍 Hybrid Search:** Utilizes Weaviate's hybrid search (Keyword + Vector) for high-precision retrieval.
* **🛡️ Scope & Relevance Checks:** Implements distance thresholding to reject out-of-scope queries (minimizing hallucinations).
* **⚡ Google Vertex AI Integration:** Powered by `gemini-1.5-flash` / `gemini-2.5-flash` for fast, cost-effective content generation.

## 🛠️ Prerequisites

Before running the project, ensure you have the following installed:

* **Docker & Docker Compose** (Required for the Weaviate local instance)
* **Python 3.8+**
* **Google Cloud API Credentials** (API Key and Project ID)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/abhisiktasingh02/weaviate-gemini-rag.git](https://github.com/abhisiktasingh02/weaviate-gemini-rag.git)
cd weaviate-gemini-rag

```

### 2. Environment Setup

Create a `.env` file in the root directory and add your Google credentials:

```ini
# .env
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_PROJECT_ID=your_google_project_id_here

```

### 3. Start Weaviate (Docker)

Start the local Weaviate vector database instance:

```bash
docker-compose up -d

```

### 4. Set Up Python Environment

Create and activate a virtual environment to keep dependencies isolated:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\activate

```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 5. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Note: Ensure you have `poppler` and `tesseract` installed on your system if you encounter errors with OCR libraries).*

## 🏃‍♂️ Usage

1. Place your target PDF file in the project directory (update the filename in the code if necessary).
2. Run the bot:

```bash
python weavebot.py

```

3. The bot will first ingest and index the document. Once finished, you will see a prompt:
> **"Hi I'm Weaviate Bot. Ask me anything related to the doc! Type 'bye' to quit)"**


4. Start asking questions!
* *Example:* "What is the capital of Utah?" (Will likely be out of scope)
* *Example:* "Summarize the carbon emission strategy." (Will retrieve from doc)



## 📁 Project Structure

```text
weaviate-gemini-rag/
├── .venv/               # Virtual environment (ignored by git)
├── .env                 # API Keys (ignored by git)
├── docker-compose.yml   # Weaviate configuration
├── requirements.txt     # Python dependencies
├── weavebot.py          # Main application logic
└── README.md            # Project documentation

```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

```

```