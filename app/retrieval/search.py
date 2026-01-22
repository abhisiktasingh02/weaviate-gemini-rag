from weaviate.classes.query import MetadataQuery

def retrieve_documents(
    collection,
    query: str,
    filters=None,
    limit: int = 5
):
    """
    Executes vector search against Weaviate.

    Returns:
        response.objects (documents)
        response.generative (optional)
    """

    response = collection.generate.near_text(
        query=query,
        filters=filters,
        limit=limit,
        return_metadata=MetadataQuery(distance=True),
    )

    return response
