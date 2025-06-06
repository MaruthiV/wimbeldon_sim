import chromadb
from typing import List, Optional
import os
from pathlib import Path

class VectorStore:
    def __init__(self, persist_directory: str = "memory_db"):
        """Initialize the vector store with ChromaDB."""
        self.persist_directory = persist_directory
        Path(persist_directory).mkdir(exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="player_memories",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_memory(self, agent_id: str, text: str):
        """Add a new memory for an agent."""
        self.collection.add(
            documents=[text],
            metadatas=[{"agent_id": agent_id}],
            ids=[f"{agent_id}_{len(self.collection.get()['ids'])}"]
        )
    
    def query(self, agent_id: str, k: int = 3) -> List[str]:
        """Query memories for a specific agent."""
        results = self.collection.query(
            query_texts=[""],  # Empty query to get all documents
            n_results=k,
            where={"agent_id": agent_id}
        )
        return results['documents'][0] if results['documents'] else []
    
    def clear_memories(self, agent_id: Optional[str] = None):
        """Clear all memories or memories for a specific agent."""
        if agent_id:
            # Delete memories for specific agent
            self.collection.delete(
                where={"agent_id": agent_id}
            )
        else:
            # Delete all memories
            self.collection.delete(
                where={}
            ) 