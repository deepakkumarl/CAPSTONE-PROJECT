import pickle
from pathlib import Path
from src.ai.vector_store import VectorStoreManager

vsm = VectorStoreManager()
if vsm.vector_store:
    print("Total chunks in loaded index:", vsm.get_total_chunks_count())
    for doc_id, doc in list(vsm.vector_store.docstore._dict.items())[:10]:
        print(f"ID: {doc_id} -> metadata: {doc.metadata}")
else:
    print("No vector store loaded.")
