import requests

# Define the API URL
url = 'http://localhost:1337/embeddings'

# Define the payload
payload = {
    "model": "llama3:7b",
    "input": [
        "I am a helpful assistant.",
        "Another example input."
    ],
    "encoding_format": "int",
    "dimensions": 4096  # Ensure this matches the collection's expected dimensionality
}

# Set the headers
headers = {
    'Content-Type': 'application/json'
}

# Call the API to retrieve embeddings
response = requests.post(url, json=payload, headers=headers)
print(len(response.json()['data'][0]['embedding']))
# Assuming response is successful and you have embeddings_list
# For illustration, assume embeddings_list is retrieved and processed
# embeddings_list = [{"embedding": [0.1] * 4096}]  # Example embedding of dimension 4096
#
# # Initialize ChromaDB client
# client = chromadb.PersistentClient(path="/Users/narayan.bansal1/Desktop/Desktop/chromaDB")
#
# # Assuming you've already created or retrieved the collection named "embeddings"
# collection = client.get_collection(name="embeddings")
#
# # Assuming embeddings_list contains embeddings and payload["input"] contains corresponding texts
# # Prepare the data for insertion into ChromaDB
# ids = []
# embeddings = []
# metadatas = []
#
# for idx, item in enumerate(embeddings_list):
#     ids.append(str(idx))
#     embeddings.append(item['embedding'])
#     metadatas.append({"text": payload["input"][idx]})
#
# # Save the embeddings in ChromaDB
# collection.add(
#     ids=ids,
#     embeddings=embeddings,
#     metadatas=metadatas
# )
#
# # Now, perform a query to retrieve embeddings
# query_texts = ["This is a query document about person"]
# n_results = 1
#
# # Query ChromaDB
# query_results = collection.query(
#     query_texts=query_texts,
#     n_results=n_results
# )
#
# # Print or process the query results
# print("Query results:")
# for result in query_results:
#     print(result)
#
# # Close the ChromaDB client
# client.close()
