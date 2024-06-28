import time

import requests
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.llms import Ollama
from langchain.schema import Document

## Lets Read the document
def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents


doc = read_doc('documnets/')
# print(doc)


## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs, chunk_size=800, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc = text_splitter.split_documents(docs)
    return doc


documents = chunk_data(docs=[Document(page_content="How much budget is allocated to agricultural sector?")])
# documents = chunk_data(doc)
# print(documents)

print(len(documents))
# print(documents)

llm = OllamaEmbeddings(model="mxbai-embed-large")

vector_embedding = llm.embed_documents(documents);
# vector_embeddings = llm.embed_documents([doc.page_content for doc in documents])
# print(llm.embed_query('How much budget is allocated to the agriculture?'));

start_time = time.time()

# print(vector_embedding[0])
# print(len(vector_embedding[0]))
#
# actual_vector = {
#     "id": "What is the color of sky?",
#     "values": vector_embedding[0]
# }
pc = Pinecone(api_key="b9656d7a-8b23-4cde-b087-f389720c92df")
index = pc.Index('langchain-vectordb')
# index.upsert(vectors=[actual_vector]);

# vectors_to_upsert = []
# for i, (doc, embedding) in enumerate(zip(documents, vector_embeddings)):
#     vector_id = f"doc_chunk_{i}"
#     actual_vector = {
#         "id": vector_id,
#         "values": embedding,
#         "metadata": {"text": doc.page_content}
#     }
#     vectors_to_upsert.append(actual_vector)
#
# index.upsert(vectors=vectors_to_upsert)

# for querying: Cosine similarity retrieve result
def retrieve_query(vector_array, k = 2):
    matching_results = index.query(
        vector=vector_array,
        top_k=k
        # include_values=True
    )

    matching_ids = [];
    for match in matching_results['matches']:
        matching_ids.append(match["id"])

    result = index.fetch(matching_ids);

    actual_result = [];
    fetch_vector = result['vectors']
    for id in matching_ids:
        val = fetch_vector[id]['metadata']['text']
        actual_result.append(val)

    print(matching_results);
    print(actual_result)

    return actual_result

from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain

model = Ollama(model="llama2");
chain = load_qa_chain(model, chain_type="stuff");

def retrieve_answers(question):
    docs = retrieve_query(vector_embedding[0], 3);
    print(docs)

    # Convert the list of strings into a list of Document objects
    doc_objects = [Document(page_content=doc, metadata={}) for doc in docs]

    # Prepare the input for the chain
    inputs = {
        "question": question,
        "input_documents": doc_objects
    }
    response = chain.invoke(inputs)
    return response

print(retrieve_answers("How much budget is allocated to agricultural sector?")['output_text'])
end_time = time.time()
print(f"Time taken to get embeddings: {end_time - start_time} seconds")
