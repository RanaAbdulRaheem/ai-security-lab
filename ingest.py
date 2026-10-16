import chromadb
from sentence_transformers import SentenceTransformer
import os

embedder = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("company_docs")

for filename in os.listdir("docs"):
    text = None
    for encoding in ["utf-8-sig", "utf-16", "latin-1"]:
        try:
            with open(f"docs/{filename}", "r", encoding=encoding) as f:
                text = f.read()
            break  # stop at the first encoding that works cleanly
        except UnicodeDecodeError:
            continue
    is_confidential = "CONFIDENTIAL" in filename
    embedding = embedder.encode(text).tolist()
    collection.add(
        ids=[filename], embeddings=[embedding], documents=[text],
        metadatas=[{"confidential": is_confidential}]
    )
print(f"Ingested {len(os.listdir('docs'))} documents.")