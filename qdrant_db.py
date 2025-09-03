import tomllib

import cohere
from qdrant_client import QdrantClient, models
from qdrant_client.models import Batch, VectorParams, Distance

MODEL = "embed-multilingual-v3.0"
MODEL_VECTOR_SIZE = 1024


def get_data() -> str:
    TEXT_TO_EMBED = "Qdrant is a vector database written in Rust"
    return TEXT_TO_EMBED


def instert_data(cohere_api_key: str, qdrant_cluster_url: str, qdrant_api_key: str, qdrant_collection_name: str):
    cohere_client = cohere.Client(cohere_api_key)
    qdrant_client = QdrantClient(
        url=qdrant_cluster_url,
        api_key=qdrant_api_key
    )

    response = qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=MODEL_VECTOR_SIZE,
            distance=Distance.DOT
        )
    )
    print(response)

    embeddings = cohere_client.embed(
        model=MODEL,
        input_type="search_document",
        texts=[TEXT_TO_EMBED]
    ).embeddings

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=Batch(
            ids=[1],
            vectors=embeddings,
        )
    )


def main():
    data_to_embed = get_data()

    with open("secrets.toml", "rb") as f:
        secrets = tomllib.load(f)

    cohere_api_key = secrets["cohere"]["api_key"]
    qdrant_api_key = secrets["qdrant"]["api_key"]
    qdrant_cluster_url = secrets["qdrant"]["cluster_url"]
    qdrant_collection_name = secrets["qdrant"]["collection_name"]

    insert_data(cohere_api_key, qdrant_api_key, qdrant_cluster_url, qdrant_collection_name)

if __name__ == "__main__":
    main()
