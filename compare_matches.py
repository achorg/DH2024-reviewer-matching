import pandas as pd


keyword_matches = pd.read_csv('DH2024WashingtonDC_reviews_2023-12-15_12-29-31.csv')
keyword_fields = ['reviewer_ID', 'reviewer_name', 'reviewer_firstname','paperID','paper_title']
keyword_matches = keyword_matches[keyword_fields]
keyword_matches['name_keyword'] = keyword_matches['reviewer_name']
keyword_matches = keyword_matches.drop('reviewer_name', axis=1)
keyword_matches['firstname_keyword'] = keyword_matches['reviewer_firstname']
keyword_matches = keyword_matches.drop('reviewer_firstname', axis=1)

semantic_matches = pd.read_csv('match_results.csv')
semantic_fields = ['personID', 'firstname', 'name', 'paperID', 'title']
semantic_matches = semantic_matches[semantic_fields]
semantic_matches['reviewer_ID'] = semantic_matches['personID']
semantic_matches = semantic_matches.drop('personID', axis=1)
semantic_matches['name_semantic'] = semantic_matches['name']
semantic_matches = semantic_matches.drop('name', axis=1)
semantic_matches['firstname_semantic'] = semantic_matches['firstname']
semantic_matches = semantic_matches.drop('firstname', axis=1)
# change personID to reviewer_ID

# get google and scholar columnds from reviewers.csv 
reviewers = pd.read_csv('reviewers.csv')
reviewers = reviewers[['personID', 'google', 'scholar']]
#change personID to reviewer_ID
reviewers['reviewer_ID'] = reviewers['personID']
# add google and scholar, match on personID
# where are the reviewer_ID and paperID columns the same?
# (i.e. where are the matches the same?)
# merged_matches = pd.merge(keyword_matches, semantic_matches, on=['reviewer_ID', 'paperID'])
#40! matches, suggests 

# for each paper, list semantic and keyword matches
# (i.e. where are the matches different?)

# merge keyword_matches and semantic_matches on reviewer_ID and paperID, include where they match and where they don't 
merged_matches = pd.merge(keyword_matches, semantic_matches, on=['reviewer_ID', 'paperID'], how='outer')
#drop title column
merged_matches = merged_matches.drop('title', axis=1)

