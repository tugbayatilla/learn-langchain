import weaviate
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("jeopardy_questions.csv", nrows = 100)
print(df.head())


with weaviate.connect_to_local(
    headers={"X-Openai-Api-Key": os.getenv("OPENAI_API_KEY")}
) as client:
    print("Weaviate client is ready:", client.is_ready())

    # Step 1: Create a Schema
    from weaviate.classes.config import Configure, Property, DataType
    JeopardyQuestion = 'JeopardyQuestion'
    if client.collections.exists(JeopardyQuestion):
        client.collections.delete(JeopardyQuestion)
        print('>>> Collection is deleted. ', JeopardyQuestion)
    
    client.collections.create("JeopardyQuestion", 
        properties=[  # Define properties
            Property(name="category", data_type=DataType.TEXT),
            Property(name="question", data_type=DataType.TEXT),
            Property(name="answer", data_type=DataType.TEXT),
    ],
    vectorizer_config=[
        Configure.NamedVectors.text2vec_openai(  # Use the "text2vec-openai" vectorizer
            name="body", source_properties=["body"]         # Set the source property(ies)
        )
    ],)

    print('>>> collection created')

    ## Step 2: Insert data into weaviate

    from weaviate.util import generate_uuid5

    jeopardy = client.collections.get(JeopardyQuestion)
    with jeopardy.batch.dynamic() as batch:
        for _, row in df.iterrows():
            question_object = {
                "category": row.category,
                "question": row.question,
                "answer": row.answer,
            }
            batch.add_object(
                properties= question_object,
                uuid=generate_uuid5(question_object)
            )
    print('>>> data imported ')

    objectsCount = len(jeopardy.query.fetch_objects().objects)
    print('>>> number of elements in ', JeopardyQuestion, ' is ', objectsCount)
    
    # Step 3: Query
    from weaviate.classes.query import MetadataQuery

    print('>>> start query')
    response = jeopardy.query.near_text(
        query="animals in movies",
        limit=2,
        include_vector=True,
        return_metadata=MetadataQuery(distance=True)
    )


    for o in response.objects:
        print(o.properties)
        print(o.metadata.distance)





