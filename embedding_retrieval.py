import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, EMBEDDING_MODEL, TOP_K_FACTS, FACT_BASE_PATH
import os
import pandas as pd


class FactRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.collection = None
        self.initialize_database()

    def initialize_database(self):
        try:
            self.collection = self.client.get_or_create_collection(
                name="facts",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error initializing collection: {e}")
            self.collection = None

    def load_facts_from_csv(self):
        try:
            df = pd.read_csv(FACT_BASE_PATH)
            facts = []
            ids = []
            metadatas = []

            for idx, row in df.iterrows():
                fact_id = str(row['id'])
                fact_text = row['fact']
                
                facts.append(fact_text)
                ids.append(fact_id)
                metadatas.append({
                    "category": str(row['category']),
                    "source": str(row['source']),
                    "date": str(row['date'])
                })

            return facts, ids, metadatas
        except Exception as e:
            print(f"Error loading facts from CSV: {e}")
            return [], [], []

    def populate_database(self):
        facts, ids, metadatas = self.load_facts_from_csv()
        
        if not facts:
            print("No facts loaded from CSV")
            return

        try:
            embeddings = self.embedding_model.encode(facts).tolist()
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=facts,
                metadatas=metadatas
            )
            print(f"Successfully populated database with {len(facts)} facts")
        except Exception as e:
            print(f"Error populating database: {e}")

    def retrieve_relevant_facts(self, claim: str, top_k: int = TOP_K_FACTS):
        try:
            if self.collection.count() == 0:
                self.populate_database()

            results = self.collection.query(
                query_texts=[claim],
                n_results=top_k
            )

            retrieved_facts = []
            distances = []
            metadatas = []

            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    retrieved_facts.append(doc)
                    distances.append(results['distances'][0][i] if results['distances'] else 0)
                    if results['metadatas']:
                        metadatas.append(results['metadatas'][0][i])

            return retrieved_facts, distances, metadatas
        except Exception as e:
            print(f"Error retrieving facts: {e}")
            return [], [], []

    def clear_database(self):
        try:
            self.client.delete_collection(name="facts")
            self.initialize_database()
            print("Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {e}")
