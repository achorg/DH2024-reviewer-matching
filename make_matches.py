import chromadb
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="LaBSE")
collection = client.get_collection(name="DH2024",embedding_function=sentence_transformer_ef)

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5,model_name="LaBSE")

papers = pd.read_csv('DH2024WashingtonDC_papers_2023-12-02_08-01-37.csv')
paper_fields = ['paperID','title', 'title_plain','keywords', 'topics', 'tg1_Language', 'tg3_Geography', 'tg2_Temporal',
'tg4_Methods', 'tg5_Disciplines_Fields_of_Study','tg7_TechReview', 'abstract_plain']
papers = papers[paper_fields]

# load reviewers, create list of dictionaries
reviewers = pd.read_csv('reviewers.csv',index_col=0)
reviewers = reviewers.to_dict('records') # --> List[dict]
# add assignment key with list for each reviewer
for reviewer in reviewers:
    reviewer['assignments'] = []

#concatenate all values in each row 
def concatenate_text(row):
    output = ""
    for field in paper_fields:
        if row[field] != 'nan':
            output += str(row[field]).replace('\n','')
    return output

documents = []
metadatas = []
ids = []
pbar = tqdm(total=len(papers))

for i, row in papers.iterrows():
    text = concatenate_text(row)
    text_chunks = splitter.split_text(text=text)
    for o, chunk in enumerate(text_chunks):
        documents.append(chunk)
        metadatas.append({"id":row["paperID"],"type": "paper", "title":row["title"]})
        ids.append(str(row["paperID"]))
        pbar.update(1)

matches = collection.query(
    query_texts=documents,
    n_results=10,
    where={"type": "person"},
)
#dict_keys(['ids', 'distances', 'metadatas', 'embeddings', 'documents', 'uris', 'data'])

# randomize order of papers
# group matches by paper id
# for each paper, get top match
# if reviewer has not reached max reviews, add to list
# record match for reviewer and paper

data = []
for i, paper in enumerate(metadatas):
    for l in range(len(matches['distances'][i])):
        row = {}
        row['paperID'] = paper["id"]
        row['title'] = paper['title']
        row['distance'] = matches['distances'][i][l]
        row["first_name"] = matches['metadatas'][i][l]["first_name"]
        row["last_name"] = matches['metadatas'][i][l]["last_name"]
        row["personID"] = matches['metadatas'][i][l]["id"]
        row["document"] = matches['documents'][i][l]
        data.append(row)
df = pd.DataFrame(data)
df.to_csv('match_results.csv')
#returns a dict with lists of lists len n_results for ids, distances, metadatas, id, documents 
#get embeddings for each paper

#use those embeddings to search for nearest reviewers

# for each paper, match N reviewers

# record results to csv with match score