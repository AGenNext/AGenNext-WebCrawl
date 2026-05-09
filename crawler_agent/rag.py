"""RAG Flow using LlamaIndex for Web Crawling Agent"""
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

# Try import - handle multiple versions
try:
    from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
    from llama_index.storage import StorageContext
    from llama_index.vector_stores import SimpleVectorStore
    LLAMA_INDEX_V3 = True
except ImportError:
    try:
        from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
        from llama_index.core.storage import StorageContext
        from llama_index.core.vector_stores import SimpleVectorStore
        LLAMA_INDEX_V3 = True
    except ImportError:
        # Try older version
        try:
            from llama_index import VectorStoreIndex, SimpleDirectoryReader
            LLAMA_INDEX_V3 = False
        except ImportError:
            LLAMA_INDEX_V3 = None


class RAGFlow:
    """RAG Flow using LlamaIndex for document Q&A"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize RAG flow
        
        Args:
            data_dir: Directory to store crawled documents
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.index = None
        self.query_engine = None
        self.llm_available = False
        
        # Check LLM availability
        self._check_llm()
    
    def _check_llm(self):
        """Check what LLMs are available"""
        try:
            from llama_index.llms import OpenAI
            self.llm_available = True
            self.llm_type = "openai"
        except ImportError:
            try:
                from llama_index.llms import Ollama
                self.llm_available = True
                self.llm_type = "ollama"
            except ImportError:
                self.llm_available = False
                self.llm_type = None
    
    def ingest_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ingest documents into RAG index
        
        Args:
            documents: List of dicts with 'text', 'metadata'
            
        Returns:
            Success status and document count
        """
        result = {"success": False, "documents_ingested": 0}
        
        try:
            # Save documents to files
            for i, doc in enumerate(documents):
                text = doc.get("text", "")
                metadata = doc.get("metadata", {})
                
                if not text:
                    continue
                
                # Create filename from metadata
                filename = metadata.get("url", f"doc_{i}").split("/")[-1]
                if not filename.endswith(".txt"):
                    filename += ".txt"
                
                filepath = self.data_dir / filename
                
                # Write document
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                
                result["documents_ingested"] += 1
            
            if result["documents_ingested"] == 0:
                result["error"] = "No documents to ingest"
                return result
            
            # Load documents
            reader = SimpleDirectoryReader(str(self.data_dir))
            docs = reader.load_data()
            
            # Create index
            if LLAMA_INDEX_V3:
                self.index = VectorStoreIndex.from_documents(docs)
            else:
                self.index = VectorStoreIndex.from_documents(docs)
            
            # Create query engine
            self.query_engine = self.index.as_query_engine()
            
            result["success"] = True
            result["indexed_documents"] = len(docs)
            
        except ImportError as e:
            result["error"] = f"llama-index not installed: {e}"
            result["hint"] = "pip install llama-index"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            question: User question
            
        Returns:
            Answer and sources
        """
        result = {"success": False, "answer": "", "sources": []}
        
        if not self.query_engine:
            result["error"] = "No index loaded. Call ingest_documents first."
            return result
        
        try:
            response = self.query_engine.query(question)
            result["answer"] = str(response)
            result["success"] = True
            
            # Try to get sources
            try:
                if hasattr(response, 'source_nodes'):
                    sources = []
                    for node in response.source_nodes:
                        sources.append({
                            "text": node.text[:200] + "...",
                            "score": node.score if hasattr(node, 'score') else None
                        })
                    result["sources"] = sources
            except:
                pass
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def ingest_crawled_data(self, crawled_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ingest crawled web pages
        
        Args:
            crawled_pages: List from crawler with 'markdown', 'url', 'metadata'
            
        Returns:
            Success status
        """
        documents = []
        
        for page in crawled_pages:
            text = page.get("markdown", "")
            url = page.get("url", "")
            
            if text:
                documents.append({
                    "text": text,
                    "metadata": {"url": url, "source": "web_crawl"}
                })
        
        return self.ingest_documents(documents)
    
    def clear_index(self):
        """Clear the index and data"""
        import shutil
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
            self.data_dir.mkdir(exist_ok=True)
        self.index = None
        self.query_engine = None


class LocalRAGFlow(RAGFlow):
    """RAG Flow with local embeddings using Ollama"""
    
    def __init__(self, data_dir: str = "./data", model: str = "llama2"):
        super().__init__(data_dir)
        self.model = model
        self._setup_local()
    
    def _setup_local(self):
        """Setup local embeddings with Ollama"""
        try:
            from llama_index.embeddings import OllamaEmbedding
            from llama_index.llms import Ollama
            
            # Use Ollama for embeddings and LLM
            embed_model = OllamaEmbedding(
                model="llama2",
                base_url="http://localhost:11434"
            )
            
            if self.index:
                self.query_engine = self.index.as_query_engine(
                    embed_model=embed_model,
                    llm=Ollama(model=self.model)
                )
            
            self.llm_available = True
            self.llm_type = "ollama"
            
        except ImportError:
            pass


# Factory function
def create_rag_flow(
    data_dir: str = "./data",
    use_local: bool = False,
    model: str = "llama2"
) -> RAGFlow:
    """
    Create RAG flow instance
    
    Args:
        data_dir: Directory for documents
        use_local: Use local Ollama (vs OpenAI)
        model: Model name for Ollama
        
    Returns:
        RAGFlow instance
    """
    if use_local:
        return LocalRAGFlow(data_dir, model)
    return RAGFlow(data_dir)