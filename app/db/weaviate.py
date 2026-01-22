import os
import weaviate
from weaviate.classes.config import Configure, Property, DataType

def get_weaviate_client():
    return weaviate.connect_to_local()

def create_schema(client):
    if "Document" in client.collections.list_all().keys():
        return
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