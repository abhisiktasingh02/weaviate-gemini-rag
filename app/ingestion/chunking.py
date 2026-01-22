import tiktoken

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