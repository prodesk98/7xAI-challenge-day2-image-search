import asyncio
import os
import base64
from uuid import uuid4

from PIL import Image
from io import BytesIO
from groq import Groq
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from langchain_openai import OpenAIEmbeddings


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
)

client_groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

client_qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

try:
    client_qdrant.create_collection(
        collection_name="images",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
except Exception as e:
    print(f"Collection already exists or error occurred: {e}")

vector_store = QdrantVectorStore(
    client=client_qdrant,
    collection_name="images",
    embedding=embeddings,
)


PROMPT_DESCRIBE_IMAGE = """You are an expert in describing images.
Given an image, provide a detailed description of its content, including objects, actions, and any relevant context. 
Your description should be clear and informative, suitable for someone who cannot see the image."""

def _generate(base64_image: str) -> str | None:
    try:
        chat_completion = client_groq.chat.completions.create(
            messages=[ # type:ignore
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT_DESCRIBE_IMAGE},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        )
        return chat_completion.choices[0].message.content
    except Exception as err:
        print(f"Error generating description: {err}")

async def generate(base64_image: str) -> str | None:
    """Generate a sample text for demonstration purposes."""
    return await asyncio.to_thread(_generate, base64_image)

def image_encode(image_file: bytes) -> str:
    """Encode an image file to a base64 string."""
    return base64.b64encode(image_file).decode('utf-8')

def convert_image_to_jpeg(image_file: bytes) -> bytes:
    """Convert an image file to JPEG format."""
    image = Image.open(BytesIO(image_file))
    output = BytesIO()
    image.convert("RGB").save(output, format="JPEG")
    return output.getvalue()

async def upload_image(file: bytes):
    """Handle image uploads and store them in the vector database."""
    image_jpeg = convert_image_to_jpeg(file)
    base64_image = image_encode(image_jpeg)
    texts = (await generate(base64_image)).split("\n")
    filename = f"uploads/img_{uuid4().hex}.jpeg"
    with open(filename, "wb") as f:
        f.write(image_jpeg)
        f.close()
    try:
        await vector_store.aadd_documents([
            Document(text, metadata={"key": filename}) for text in texts if text
        ])
    except Exception as err_:
        print(f"Error uploading image: {err_}")


async def search_image(query: str):
    """Search for images based on a query."""
    try:
        results = await vector_store.asimilarity_search_with_score(query, k=25)
        return results
    except Exception as err:
        print(f"Error searching for images: {err}")
        return []