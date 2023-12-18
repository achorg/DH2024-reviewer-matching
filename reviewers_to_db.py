import chromadb
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from chromadb.utils import embedding_functions
import uuid

client = chromadb.PersistentClient(path="reviewers")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="LaBSE"
)
collection = client.get_or_create_collection(
    name="reviewers", embedding_function=sentence_transformer_ef
)

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5, model_name="LaBSE")

reviewer_fields = ['title','full_text','first_name','last_name', 'personID','topics', 'maxreviews']
reviewer_df = pd.read_csv("reviewers.csv")
reviewer_papers = pd.read_csv("dh24_papers.csv")
# change 'topics_x' to 'topics'
reviewer_papers = reviewer_papers.rename(columns={'topics_x':'topics'})

#join reviewer_df and reviewer_papers
reviewer_df = pd.concat([reviewer_df, reviewer_papers])
def concatenate_text(row):
    output = ""
    for field in ["topics", "title", "full_text"]:
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
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "title": row["title"],
            }
        )
        ids.append(uuid.uuid4().hex)
        pbar.update(1)

collection.add(documents=documents, metadatas=metadatas, ids=ids)
