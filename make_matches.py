import chromadb
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from chromadb.utils import embedding_functions
import random 

client = chromadb.PersistentClient(path="db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="LaBSE")
collection = client.get_collection(name="DH2024",embedding_function=sentence_transformer_ef)

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5,model_name="LaBSE")

papers = pd.read_csv('DH2024WashingtonDC_papers_2023-12-02_08-01-37.csv')
paper_fields = ['paperID','title', 'title_plain','keywords', 'topics', 'tg1_Language', 'tg3_Geography', 'tg2_Temporal',
'tg4_Methods', 'tg5_Disciplines_Fields_of_Study','tg7_TechReview', 'abstract_plain']
papers = papers[paper_fields]

# load reviewers, create list of dictionaries
reviewers = pd.read_csv('reviewers.csv')
reviewers = reviewers.to_dict('records') # --> List[dict]
# add assignment key with list for each reviewer
for reviewer in reviewers:
    reviewer['assignments'] = []

#concatenate all values in each row 
def concatenate_text(row):
    """
    Concatenates the non-null values from the specified fields in the given row.

    """
    output = ""
    for field in paper_fields:
        if row[field] != 'nan':
            output += str(row[field]).replace('\n','')
    return output

documents = []
metadatas = []
ids = []

for i, row in papers.iterrows():
    text = concatenate_text(row)
    text_chunks = splitter.split_text(text=text)
    for o, chunk in enumerate(text_chunks):
        documents.append(chunk)
        metadatas.append({"id":row["paperID"],"type": "paper", "title":row["title"]})
        ids.append(str(row["paperID"]))

matches = collection.query(
    query_texts=documents,
    n_results=10,
    where={"type": "person"},
)
#dict_keys(['ids', 'distances', 'metadatas', 'embeddings', 'documents', 'uris', 'data'])
data = []
for i, (distance, meta) in enumerate(zip(matches['distances'], matches['metadatas'])):
    for d, m in zip(distance, meta):
        data.append({"paperID": metadatas[i]['id'],"title":metadatas[i]['title'], "personID": m['id'], "distance": d, 'first_name': m['first_name'], 'last_name': m['last_name']})

matches_df = pd.DataFrame(data)

random_paperIDs = matches_df.paperID.unique()
random.shuffle(random_paperIDs)

for id in random_paperIDs:
    reviews_assigned = 0
    
    paper_matches = matches_df[matches_df['paperID'] == id]
    # sort by distance in descending order
    paper_matches = paper_matches.sort_values(by=['distance'],ascending=False)
    for i, row in paper_matches.iterrows():
        reviewer = next((item for item in reviewers if item["personID"] == row['personID']), None)
        if reviewer:
            # if reviewer has less than max reviews and paper has less than 3 reviews
            if len(reviewer['assignments']) < reviewer['maxreviews'] and reviews_assigned < 3:
                reviewer['assignments'].append({'paperID':row['paperID'],'title':row['title'],'distance':row['distance']})
                reviews_assigned += 1

output = []
for reviewer in reviewers:
    for assignment in reviewer['assignments']:
        output.append({'personID':reviewer['personID'],'firstname':reviewer['firstname'],'name':reviewer['name'],'paperID':assignment['paperID'],'title':assignment['title'],'distance':assignment['distance']})
out_df = pd.DataFrame(output)
out_df.to_csv('match_results.csv')
