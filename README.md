# weaviate-gemini-rag
A RAG chatbot using Weaviate and Google Gemini to chat with PDFs. 
Features multimodal ingestion (text, tables, OCR), intelligent query parsing, and strict scope checking to reduce hallucinations.

1. Multimodal Ingestion: Extracts text, tables, and performs OCR on images from PDFs using pdfplumber and pytesseract.
2. Intelligent Query Parsing: Uses Gemini to pre-process user queries, extracting search intent (lookup vs. explanation) and keywords before searching.
3. Hybrid Search: Leverages Weaviate's hybrid search (Keyword + Vector) for high-precision retrieval.
4. Scope & Relevance Checks: Includes distance thresholding to reject out-of-scope queries (minimizing hallucinations).
5. Google Vertex AI Integration: Powered by gemini-1.5-flash / gemini-2.5-flash for fast, cost-effective generation.
