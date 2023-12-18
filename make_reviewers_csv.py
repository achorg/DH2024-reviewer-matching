import pandas as pd
from tqdm import tqdm

#Load data from the Index of Digital Humanities Conferences
works = pd.read_csv('dh_conferences_data/works.csv')
#{'id': 4, 'conference': 1, 'title': 'The Middle English Grammar Project', 'work_type': 1.0, 'full_text':}
authorships = pd.read_csv('dh_conferences_data/authorships.csv')
#"id","author","work","authorship_order","appellation"

# merge works and authorships on work
merged = pd.merge(works, authorships, left_on='id', right_on='work', how='left')
# change author to int 
merged['author'] = merged['author'].fillna(0).astype(int)
#"id","author","work","authorship_order","appellation"

# names from appelations.csv
appelations = pd.read_csv('dh_conferences_data/appellations.csv')
# join appelations and merged on author
merged = pd.merge(merged, appelations, left_on='appellation', right_on='id', how='left')


reviewers = pd.read_csv("DH2024WashingtonDC_reviewers_2023-12-17_18-56-09.csv")
reviewer_fields = ["personID", "name", "firstname", "topics", "maxreviews"]
reviewer_df = reviewers[reviewer_fields]

# only 147 have a maxreviews, set default of 3
reviewer_df["maxreviews"] = reviewer_df["maxreviews"].fillna(3)

# for each reviewer add a row for each paper in the Index 

# match 'first_name' 'last_name' in merged with 'name', 'firstname' in reviewer_df
all_reviewers = pd.merge(merged, reviewer_df, left_on=['first_name', 'last_name'], right_on=['firstname', 'name'], how='right')
r_fields = ['personID','first_name','last_name','title','full_text', 'topics', 'maxreviews']
all_reviewers = all_reviewers[r_fields]
all_reviewers.to_csv("reviewers.csv", index=False)

# add reviewer's papers from the current conference 
dh24_papers = pd.read_csv("DH2024WashingtonDC_papers_2023-12-17_19-22-02.csv")
# create rows for papers with many authors separated by ; 
dh24_papers['authors'] = dh24_papers['authors'].str.split(';')
# if len of authors > 1, create a row for each author
dh24_papers = dh24_papers.explode('authors')
# remove \n from all authors
dh24_papers['authors'] = dh24_papers['authors'].str.replace('\n', '')
# add column for first_name and last_name
dh24_papers['first_name'] = dh24_papers['authors'].str.split(',').str[-1]
dh24_papers['last_name'] = dh24_papers['authors'].str.split(',').str[0]
# strip whitespace from first_name and last_name
dh24_papers['first_name'] = dh24_papers['first_name'].str.strip()
dh24_papers['last_name'] = dh24_papers['last_name'].str.strip()
# replace 'title' with 'title_plain'
dh24_papers['title'] = dh24_papers['title_plain']
# remove 'title_plain'
dh24_papers = dh24_papers.drop(columns=['title_plain']) 
# change 'abstract_plain' to 'full_text'
dh24_papers = dh24_papers.rename(columns={'abstract_plain':'full_text'})
# add 'maxreviews' column
dh24_papers = dh24_papers[['title','full_text','first_name','last_name', 'topics']]

# get dh24_papers where first_name and last_name are in reviewer_df
dh24_papers = pd.merge(dh24_papers, reviewer_df, left_on=['first_name', 'last_name'], right_on=['firstname', 'name'], how='right')
# drop where title nan
dh24_papers = dh24_papers.dropna(subset=['title'])
r_fields = ['personID','first_name','last_name','title','full_text', 'topics_x', 'maxreviews']
dh24_papers = dh24_papers[r_fields]

dh24_papers.to_csv("dh24_papers.csv", index=False)
