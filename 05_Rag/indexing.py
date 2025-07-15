from dotenv import load_dotenv
import os
load_dotenv()
from pathlib import Path

import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore


api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

pdf_path = Path(__file__).parent / "nodejs.pdf"

#loading chunking
loader = PyPDFLoader(file_path = pdf_path)
docs = loader.load()

print("docs[0]",docs[5])

#Chunking
# docs[0].split("\n")ye ham krte but naa kro ab ye khud hi hoga langchain krenge

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400,
)
split_docs = text_splitter.split_documents(documents =docs)


#vector embedder

embedding_model  = GoogleGenerativeAIEmbeddings(
    model = "models/embedding-001",
   google_api_key=os.getenv("GOOGLE_API_KEY")
)

#using [embedding_model] create [embeddings] of [split_docs] 

vector_store=  QdrantVectorStore.from_documents(
    documents = split_docs,
    url="http://localhost:6333",
    collection_name = "learning_vectors",
    embedding=embedding_model
)
print("indexing of document done")