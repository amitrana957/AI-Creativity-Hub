import chromadb
from models import hf_embeddings
from .test_data import employees


# Creating an instance of ChromaClient to establish a connection with the Chroma database
client = chromadb.Client()

collection_name = "employee_collection"


# Defining a function named 'main'
# This function is used to encapsulate the main operations for creating collections,
# generating embeddings, and performing similarity search
def main():
    try:
        # Code for database operations will be placed here
        # This includes creating collections, adding data, and performing searches

        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "Collection for employees"},
            configuration={"embedding_function": hf_embeddings},
        )

        employee_documents = []
        for employee in employees:
            document = f"{employee['role']} with {employee['experience']} years of experience in {employee['department']}. "
            document += (
                f"Skills: {employee['skills']}. Located in {employee['location']}. "
            )
            document += f"Employment type: {employee['employment_type']}."
            employee_documents.append(document)

        collection.add(
            # Extracting employee IDs to be used as unique identifiers for each record
            ids=[employee["id"] for employee in employees],
            # Using the comprehensive text documents we created
            documents=employee_documents,
            # Adding comprehensive metadata for filtering and search
            metadatas=[
                {
                    "name": employee["name"],
                    "department": employee["department"],
                    "role": employee["role"],
                    "experience": employee["experience"],
                    "location": employee["location"],
                    "employment_type": employee["employment_type"],
                }
                for employee in employees
            ],
        )

        all_items = collection.get()
        # Logging the retrieved items to the console for inspection or debugging
        print("Collection contents:")
        print(f"Number of documents: {len(all_items['documents'])}")
        perform_advanced_search(collection, all_items)

    except Exception as error:
        # Catching and handling any errors that occur within the 'try' block
        # Logs the error message to the console for debugging purposes
        print(f"Error: {error}")


def perform_advanced_search(collection, all_items):
    try:
        print("=== Similarity Search Examples ===")
        # Example 1: Search for Python developers
        print("\n1. Searching for Python developers:")
        query_text = "Python developer with web development experience"
        results = collection.query(query_texts=[query_text], n_results=3)
        print(f"Query: '{query_text}'")
        rs = enumerate(
            zip(results["ids"][0], results["documents"][0], results["distances"][0])
        )
        print(f"{results} {50*'==='}\n\n {list(rs)} \n\n{50*'==='}")
        for i, (doc_id, document, distance) in rs:
            metadata = results["metadatas"][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(
                f"     Role: {metadata['role']}, Department: {metadata['department']}"
            )
            print(f"     Document: {document[:100]}...")

        # Example 2: Search for leadership roles
        print("\n2. Searching for leadership and management roles:")
        query_text = "team leader manager with experience"
        results = collection.query(query_texts=[query_text], n_results=3)
        print(f"Query: '{query_text}'")
        for i, (doc_id, document, distance) in enumerate(
            zip(results["ids"][0], results["documents"][0], results["distances"][0])
        ):
            metadata = results["metadatas"][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(
                f"     Role: {metadata['role']}, Experience: {metadata['experience']} years"
            )

        print("\n=== Metadata Filtering Examples ===")
        # Example 1: Filter by department
        print("\n3. Finding all Engineering employees:")
        results = collection.get(where={"department": "Engineering"})
        print(f"Found {len(results['ids'])} Engineering employees:")
        for i, doc_id in enumerate(results["ids"]):
            metadata = results["metadatas"][i]
            print(
                f"  - {metadata['name']}: {metadata['role']} ({metadata['experience']} years)"
            )
        # Example 2: Filter by experience range
        print("\n4. Finding employees with 10+ years experience:")
        results = collection.get(where={"experience": {"$gte": 10}})
        print(f"Found {len(results['ids'])} senior employees:")
        for i, doc_id in enumerate(results["ids"]):
            metadata = results["metadatas"][i]
            print(
                f"  - {metadata['name']}: {metadata['role']} ({metadata['experience']} years)"
            )
        # Example 3: Filter by location
        print("\n5. Finding employees in California:")
        results = collection.get(
            where={"location": {"$in": ["San Francisco", "Los Angeles"]}}
        )
        print(f"Found {len(results['ids'])} employees in California:")
        for i, doc_id in enumerate(results["ids"]):
            metadata = results["metadatas"][i]
            print(f"  - {metadata['name']}: {metadata['location']}")

        print("\n=== Combined Search: Similarity + Metadata Filtering ===")
        # Example: Find experienced Python developers in specific locations
        print("\n6. Finding senior Python developers in major tech cities:")
        query_text = "senior Python developer full-stack"
        results = collection.query(
            query_texts=[query_text],
            n_results=5,
            where={
                "$and": [
                    {"experience": {"$gte": 8}},
                    {"location": {"$in": ["San Francisco", "New York", "Seattle"]}},
                ]
            },
        )
        print(f"Query: '{query_text}' with filters (8+ years, major tech cities)")
        print(f"Found {len(results['ids'][0])} matching employees:")
        for i, (doc_id, document, distance) in enumerate(
            zip(results["ids"][0], results["documents"][0], results["distances"][0])
        ):
            metadata = results["metadatas"][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(
                f"     {metadata['role']} in {metadata['location']} ({metadata['experience']} years)"
            )
            print(f"     Document snippet: {document[:80]}...")

        # Check if the results are empty or undefined
        if not results or not results["ids"] or len(results["ids"][0]) == 0:
            # Log a message if no similar documents are found for the query term
            print(f'No documents found similar to "{query_text}"')
            return

        # Log the header for the top 3 similar documents based on the query term
        print(f'Top 3 similar documents to "{query_text}":')
        # Loop through the top 3 results and log the document details
        for i in range(min(3, len(results["ids"][0]))):
            # Extract the document ID and similarity score from the results
            doc_id = results["ids"][0][i]
            score = results["distances"][0][i]
            # Retrieve the document text corresponding to the current ID from the results
            text = results["documents"][0][i]
            # Check if the text is available; if not, log 'Text not available'
            if not text:
                print(
                    f' - ID: {doc_id}, Text: "Text not available", Score: {score:.4f}'
                )
            else:
                print(f' - ID: {doc_id}, Text: "{text}", Score: {score:.4f}')
    except Exception as error:
        print(f"Error in advanced search: {error}")


main()
