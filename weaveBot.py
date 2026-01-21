import weaviate
import os
import dotenv
from weaviate.classes.config import Configure, Property, DataType
import fitz
import pdfplumber
from PIL import Image
import tiktoken
from pypdf import PdfReader
import pytesseract
import json
import re
from weaviate.classes.query import Filter, MetadataQuery
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(os.getenv("LLM_MODEL"))
pdf_path = "Apples_Product_Use_Electricity_Strategy.pdf"

parsed = {
  "semantic_query": "Weaviate architecture diagram shard HNSW",
  "modality": "image",
  "intent": "explanation",
  "keywords": ["Weaviate", "architecture", "diagram", "HNSW"],
  "filters": {}
}

def build_filters(parsed):
    filters = None
    if parsed["modality"] != "any":
        filters = Filter.by_property("modality").equal(parsed["modality"])
    return filters

QUERY_PARSER_SYSTEM_PROMPT = """
You are a query parser for a vector search system.

Extract structured search intent from the user query.

Return ONLY valid JSON with these fields:
- semantic_query: string (rewritten query for semantic search)
- modality: one of ["text", "image", "table", "any"]
- intent: one of ["definition", "explanation", "comparison", "lookup", "summary"]
- keywords: list of important keywords
- filters: object (may be empty)

Do NOT add any extra text.
"""

def safe_json_parse(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())


def parse_user_query(user_query: str) -> dict:
    prompt = f"""
    {QUERY_PARSER_SYSTEM_PROMPT}
    User query:
    {user_query}
    """
    response = model.generate_content(prompt)
    return safe_json_parse(response.text)

def chunk_text(text, max_tokens=500, overlap=50):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunks.append(encoding.decode(tokens[start:end]))
        start = end - overlap
    return chunks

def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for pageno, page in enumerate(pdf.pages):
            for table in page.extract_tables():
                tables.append({
                    "page": pageno + 1,
                    "table": table
                })
    return tables

def extract_text(pdf_path):
    reader=PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        pages.append({
            "page": i + 1,
            "text": text
        })
    return pages

def extract_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    
    for page_index in range(len(doc)):
        page = doc[page_index]
        for img in page.get_images(full=True):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                img_pil = Image.frombytes(
                    "RGB", [pix.width, pix.height], pix.samples
                )
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img_pil = Image.frombytes(
                    "RGB", [pix.width, pix.height], pix.samples
                )
            images.append((page_index + 1, img_pil))
    return images

def orc_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default

    
with weaviate.connect_to_local() as client:
    for name in client.collections.list_all().keys():
        client.collections.delete(name)

    client.collections.create(
        name="Document",

        properties=[
            Property(name="content", data_type=DataType.TEXT),
            Property(name="modality", data_type=DataType.TEXT),
            Property(name="source", data_type=DataType.TEXT),
            Property(name="page", data_type=DataType.INT),
            Property(name="caption", data_type=DataType.TEXT),
        ],

        vector_config=Configure.Vectors.text2vec_google_vertex(
            project_id=os.getenv("GOOGLE_PROJECT_ID"),
            model="gemini-embedding-001",
        ),

        generative_config=Configure.Generative.google_vertex(
            project_id=os.getenv("GOOGLE_PROJECT_ID"),
            model_id="gemini-2.5-flash",
        ),
    )
    
    pdf_path = input("Enter the path to the PDF document: ").strip()
    text_pages = extract_text(pdf_path)
    table_pages = extract_tables(pdf_path)
    image_pages = extract_images(pdf_path)
    collection = client.collections.use("Document")
    
    with collection.batch.fixed_size(batch_size=50) as batch:
        for item in text_pages:
            page = item["page"]
            text = item["text"]

            if not text or not text.strip():
                continue

            for chunk in chunk_text(text):
                batch.add_object({
                    "content": chunk,
                    "modality": "text",
                    "source": os.path.basename(pdf_path),
                    "page": safe_int(page),
                })
        for page, table_summary in table_pages:
            batch.add_object({
                "content": str(table_summary),
                "modality": "table",
                "source": os.path.basename(pdf_path),
                "page": safe_int(page),
                "caption": "Extracted table",
            })
        for page, image in image_pages:
            try:
                text = orc_image(image)
            except Exception:
                continue
            if text.strip():
                batch.add_object({
                    "content": text,
                    "modality": "image",
                    "source": os.path.basename(pdf_path),
                    "page": safe_int(page),
                    "caption": "Extracted text from image",
                })
        print("Finished inserting document data.")
        print("Hi I'm Weaviate Bot. Ask me anything related to the doc! Type 'bye' to quit) ")
        
        while True:
            user_query = input("Enter your query (or type 'bye' to quit): ")

            if user_query.lower() == "bye":
                print("Exiting search.")
                break

            if not user_query:
                print("Please enter a non-empty query.")
                continue 

            try:
                parsed = parse_user_query(user_query)
                filters = build_filters(parsed)
            except Exception as e:
                print(f"Error parsing query: {e}")
                continue

            print(f"DEBUG -> Intent: {parsed['intent']} | Semantic Query: {parsed['semantic_query']}")


            response = collection.generate.near_text(
                query=parsed["semantic_query"],
                filters=filters,
                limit=5,
                return_metadata=MetadataQuery(distance=True),
                grouped_task=f"""
                    Intent: {parsed['intent']}
                    User Query: {user_query}
                    
                    Task: Answer the user's question using the provided context.
                    
                    Guidelines:
                    1. Use the provided context to answer.
                    2. If the context describes specific strategies (e.g., for a specific company or product), use those as examples to answer the query.
                    3. Do NOT simply say "I don't know" unless the context is completely unrelated (e.g., cooking recipes vs carbon emissions).
                    4. Synthesize the answer from the fragments provided.
                """
            )
            if not response.objects:
                print("Bot: I don't know (No relevant documents found).")
                print("-" * 40)
                continue

            top_distance = response.objects[0].metadata.distance
            THRESHOLD = 0.5 

            if top_distance > THRESHOLD:
                print(f"Bot: I don't know. (Topic seems out of scope. Distance: {top_distance:.2f})")
                print("-" * 40)
                continue

            if response.generative:
                print(f"Bot: {response.generative.text}")
                
                pages = sorted(list(set([o.properties["page"] for o in response.objects])))
                print(f"\n[Source Pages: {pages} | Relevance Score: {1 - top_distance:.2f}]")
            else:
                print("Bot: No answer generated.")

            print("-" * 40)