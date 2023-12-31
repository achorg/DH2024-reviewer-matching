import chromadb
import pandas as pd
from tqdm import tqdm
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from chromadb.utils import embedding_functions
import random 

client = chromadb.PersistentClient(path="reviewers")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="LaBSE")
collection = client.get_collection(name="reviewers",embedding_function=sentence_transformer_ef)

splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=5,model_name="LaBSE")

papers = pd.read_csv('DH2024WashingtonDC_papers_2023-12-17_20-31-56.csv')
paper_fields = ['paperID','authors','title','contribution_type','title_plain','keywords', 'topics', 'tg1_Language', 'tg3_Geography', 'tg2_Temporal',
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
        metadatas.append({"id":row["paperID"],"type": "paper", "title":row["title"],"abstract":row['abstract_plain'], 'paper_topics':row['topics'], 'contribution_type': row['contribution_type']})
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
        try:
            data.append({"paperID": metadatas[i]['id'],"title":metadatas[i]['title'], 'paper_topics': metadatas[i]['paper_topics'],'abstract':metadatas[i]['abstract'],'contribution_type': metadatas[i]['contribution_type'], "personID": m['id'], "distance": d, 'first_name': m['first_name'], 'last_name': m['last_name']})
        except Exception as e:
            print(e)
matches_df = pd.DataFrame(data)

random_paperIDs = matches_df.paperID.unique()
random.shuffle(random_paperIDs)

for id in random_paperIDs:
    reviews_assigned = 0
    
    paper_matches = matches_df[matches_df['paperID'] == id]
    # sort by distance in ascending order, closest matches first.
    paper_matches = paper_matches.sort_values(by=['distance'])
    for i, row in paper_matches.iterrows():
        reviewer = next((item for item in reviewers if item["personID"] == row['personID']), None)
        if reviewer:
            # if reviewer has less than max reviews and paper has less than 4 reviews
            if len(reviewer['assignments']) < reviewer['maxreviews'] and reviews_assigned < 4:
                # assert reviewer is not already assigned to this paper
                if not any(d['paperID'] == row['paperID'] for d in reviewer['assignments']):
                    # assert reviewer is not an author of this paper
                    reviewer_name = row['last_name'] + ", " + row['first_name']
                    authors = papers[papers['paperID'] == row['paperID']]['authors'].values[0]
                    if reviewer_name not in authors:
                        reviewer['assignments'].append({'paperID':row['paperID'],'contribution_type': row['contribution_type'],'title':row['title'],'paper_topics':row['paper_topics'],'abstract':row['abstract'],'distance':row['distance']})
                        reviews_assigned += 1

output = []
for reviewer in reviewers:
    for assignment in reviewer['assignments']:
        output.append({'personID':reviewer['personID'],'first_name':reviewer['first_name'],'last_name':reviewer['last_name'],'reviewer_topics':str(reviewer['topics']).replace(',','').replace('\n',';'),'paperID':assignment['paperID'],'title':assignment['title'],'abstract':assignment['abstract'],'paper_topics':str(assignment['paper_topics']).replace('\n',';'),'distance':assignment['distance'], 'contribution_type': assignment['contribution_type']})
out_df = pd.DataFrame(output)
out_df['keyword_matches'] = out_df.apply(lambda row: ";".join(list(set(row['paper_topics'].split(';')) & set(row['reviewer_topics'].split(';')))), axis=1)
out_df['number_of_matches'] = out_df.apply(lambda row: len(set(row['paper_topics'].split(';')) & set(row['reviewer_topics'].split(';'))), axis=1)
out_df.to_csv('match_results.csv')
