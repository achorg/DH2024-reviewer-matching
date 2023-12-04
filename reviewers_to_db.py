import chromadb
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from chromadb.utils import embedding_functions
import uuid

client = chromadb.PersistentClient(path="db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="LaBSE"
)
collection = client.get_or_create_collection(
    name="DH2024", embedding_function=sentence_transformer_ef
)

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5, model_name="LaBSE")

reviewer_fields = ["personID", "name", "firstname", "topics", "maxreviews"]
reviewer_df = pd.read_csv("reviewers.csv")


def concatenate_text(row):
    output = ""
    for field in ["topics", "google", "scholar"]:
        if row[field] != "nan":
            output += str(row[field]).replace("\n", "")
    return output


documents = []
metadatas = []
ids = []
pbar = tqdm(total=len(reviewer_df))

for i, row in reviewer_df.iterrows():
    text = concatenate_text(row)
    text_chunks = splitter.split_text(text=text)
    for o, chunk in enumerate(text_chunks):
        documents.append(chunk)
        metadatas.append(
            {
                "id": row["personID"],
                "type": "person",
                "first_name": row["firstname"],
                "last_name": row["name"],
            }
        )
        ids.append(uuid.uuid4().hex)
        pbar.update(1)

collection.add(documents=documents, metadatas=metadatas, ids=ids)
