import google.generativeai as genai
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
#vector embedder
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


embedding_model  = GoogleGenerativeAIEmbeddings(
    model = "models/embedding-001",
)
#connetion to Database
vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name = "learning_vectors",
    embedding=embedding_model
)
#take user query

while True:
    query = input("> ")

    #Vector Similarity search in DB QdrantDb Same database only
    search_results = vector_db.similarity_search(
        query=query
    )
    # print("search result",search_results)
    context ="\n\n\n".join([f"Page content :{result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']} " for result in search_results])
    SYSTEM_PROMPT = f"""
    you are a helpful AI assistant who answer query based on the available context retrieved from a PDF file along with page_contents and page number.
    You should only ans the user based on the following context and show the code given in the context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")


    response = model.generate_content(
        [SYSTEM_PROMPT, query]
    )


    print(f"\n🤖: {response.text}")
