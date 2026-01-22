import os
from app.db.weaviate import get_weaviate_client, create_schema
from app.guardrails.relevance import is_relevant
from app.ingestion.text import extract_text
from app.ingestion.tables import extract_tables
from app.ingestion.images import extract_images, orc_image
from app.ingestion.chunking import chunk_text
from app.query.filters import build_filters
from app.query.parser import parse_user_query
from app.retrieval.search import retrieve_documents
from app.utils.helpers import safe_int
from app.generation.answer import generate_answer

def main():
    with get_weaviate_client() as client:
        create_schema(client)
        collection = client.collections.use("Document")
        
        pdf_path = input("Enter the path to the PDF document: ").strip()
        
        text_pages = extract_text(pdf_path)
        table_pages = extract_tables(pdf_path)
        image_pages = extract_images(pdf_path)
        populate_db(collection, pdf_path, text_pages, table_pages, image_pages)
        
        print("\n🤖 Hi I'm Weaviate Bot. Ask me anything related to the doc! Type 'bye' to quit\n")

        while True:
            user_query = input("Query> ").strip()

            if user_query.lower() == "bye":
                print("Goodbye 👋")
                break

            if not user_query:
                print("Please enter a non-empty query.")
                continue

            try:
                parsed = parse_user_query(user_query)
                filters = build_filters(parsed)
            except Exception as e:
                print(f"Query parsing failed: {e}")
                continue

            print(
                f"DEBUG → intent={parsed['intent']} | semantic_query={parsed['semantic_query']}"
            )

            retrieval_response = retrieve_documents(
                collection,
                query=parsed["semantic_query"],
                filters=filters,
            )

            if not retrieval_response.objects:
                print("Bot: No relevant context found.")
                print("-" * 40)
                continue

            top_distance = retrieval_response.objects[0].metadata.distance

            if not is_relevant(top_distance):
                print(
                    f"Bot: Out of scope (distance={top_distance:.2f})"
                )
                print("-" * 40)
                continue

            # 🧠 GENERATION (USING SAME CONTEXT)
            final_answer = generate_answer(
                retrieved_objects=retrieval_response.objects,
                user_query=user_query,
                intent=parsed["intent"],
            )

            print(f"\nBot: {final_answer}")

            pages = sorted(
                {obj.properties["page"] for obj in retrieval_response.objects}
            )
            print(f"[Source Pages: {pages} | Relevance Score: {1 - top_distance:.2f}]")
            print("-" * 40)

def populate_db(collection, pdf_path, text_pages, table_pages, image_pages):
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
        
if __name__ == "__main__":
    main()