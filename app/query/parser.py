from app.config.prompts import QUERY_PARSER_SYSTEM_PROMPT
from app.config.settings import MODEL
from app.utils.json_utils import safe_json_parse

parsed = {
  "semantic_query": "Weaviate architecture diagram shard HNSW",
  "modality": "image",
  "intent": "explanation",
  "keywords": ["Weaviate", "architecture", "diagram", "HNSW"],
  "filters": {}
}

def parse_user_query(user_query: str) -> dict:
    prompt = f"""
    {QUERY_PARSER_SYSTEM_PROMPT}
    User query:
    {user_query}
    """
    response = MODEL.generate_content(prompt)
    return safe_json_parse(response.text)