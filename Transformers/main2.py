# import langchain
import time

import requests
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.embeddings.openai import OpenAIEmbeddings

## Lets Read the document
def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents


doc = read_doc('documnets/')
print(doc)


## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc = text_splitter.split_documents(docs)
    return doc


documents = chunk_data(docs=doc)
print(documents)


# Function to extract text from document chunks
def extract_text_from_chunks(doc_chunks):
    texts = [chunk.page_content for chunk in doc_chunks]
    return texts


texts = extract_text_from_chunks(documents)
print(texts)


def get_embeddings(documents):
    # Define the API URL
    url = 'http://localhost:1337/embeddings'

    # Define the payload
    payload = {
        "model": "llama3:7b",
        "input": documents,
        "encoding_format": "int",
        "dimensions": 4096  # Ensure this matches the collection's expected dimensionality
    }

    # Set the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Call the API to retrieve embeddings
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()['data'][0]['embedding']


start_time = time.time()
# get_embeddings(texts)
end_time = time.time()
print(f"Time taken to get embeddings: {end_time - start_time} seconds")
# Vector Search DB In Pinecone
# pc = Pinecone(
#     api_key="b9656d7a-8b23-4cde-b087-f389720c92df",
#     # environment="gcp-starter"
# )
# index_name = "langchain-vectordb"
# index=Pinecone.from_documents(doc,embeddings,index_name=index_name)

pc = Pinecone(api_key='b9656d7a-8b23-4cde-b087-f389720c92df')
index = pc.Index('langchain-vectordb')
