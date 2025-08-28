import tomllib
import cohere
from qdrant_client import QdrantClient, models
from qdrant_client.models import Batch, VectorParams, Distance

def main():
    try:
        with open("secrets.toml", "rb") as f:
            secrets = tomllib.load(f)
    except FileNotFoundError:
        print("Ошибка: Файл secrets.toml не найден!")
        return
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        return

    try:
        cohere_client = cohere.Client(secrets["cohere"]["api_key"])
        qdrant_client = QdrantClient(
            url=secrets["qdrant"]["cluster_url"],
            api_key=secrets["qdrant"].get("api_key")
        )
    except Exception as e:
        print(f"Ошибка инициализации клиентов: {e}")
        return

    COLLECTION_NAME = "MyCollection"
    TEXT_TO_EMBED = "Qdrant is a vector database written in Rust"

    try:
        collections = qdrant_client.get_collections().collections
        existing_collections = [col.name for col in collections]
        
        if COLLECTION_NAME not in existing_collections:
            print(f"Создаем коллекцию '{COLLECTION_NAME}'...")
            
            test_embedding = cohere_client.embed(
                model="embed-english-v3.0",
                input_type="search_document",
                texts=["test"]
            ).embeddings[0]
            
            vector_size = len(test_embedding)
            print(f"Размерность векторов: {vector_size}")
            
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Коллекция '{COLLECTION_NAME}' успешно создана!")
        else:
            print(f"Коллекция '{COLLECTION_NAME}' уже существует")
            
    except Exception as e:
        print(f"Ошибка работы с коллекцией: {e}")
        return

    try:
        print("Генерируем эмбеддинги...")
        embeddings = cohere_client.embed(
            model="embed-english-v3.0",
            input_type="search_document",
            texts=[TEXT_TO_EMBED]
        ).embeddings
        print("Эмбеддинги успешно сгенерированы")
        
    except Exception as e:
        print(f"Ошибка генерации эмбеддингов: {e}")
        return

    try:
        print("Добавляем данные в коллекцию...")
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=Batch(
                ids=[1],
                vectors=embeddings,
            )
        )
        print("Данные успешно добавлены в коллекцию!")
        
    except Exception as e:
        print(f"Ошибка добавления данных: {e}")
        return
    
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        print(f"\nИнформация о коллекции:")
        print(f"Имя: {COLLECTION_NAME}")
        print(f"Размерность: {collection_info.config.params.vectors.size}")
        print(f"Количество точек: {collection_info.points_count}")
        
        count_result = qdrant_client.count(collection_name=COLLECTION_NAME)
        print(f"Подтвержденное количество точек: {count_result.count}")
        
    except Exception as e:
        print(f"Ошибка получения информации: {e}")

if __name__ == "__main__":
    main()