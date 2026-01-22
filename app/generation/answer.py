def generate_answer(retrieved_objects, user_query: str, intent: str) -> str:
    """
    Generate grounded answer from retrieved Weaviate objects.
    """

    context = "\n\n".join(
        obj.properties["content"] for obj in retrieved_objects
    )

    prompt = f"""
    Intent: {intent}
    User Question: {user_query}

    Context:
    {context}

    Rules:
    - Answer ONLY from the context above
    - If context is insufficient, say so
    - Be concise and factual
    """

    from app.config.settings import MODEL
    response = MODEL.generate_content(prompt)

    return response.text.strip()
