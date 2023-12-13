import pandas as pd


keyword_matches = pd.read_csv('DH2024WashingtonDC_reviews_2023-12-13_11-53-38.csv')
keyword_fields = ['reviewer_ID', 'reviewer_name', 'reviewer_firstname','paperID','paper_title']
keyword_matches = keyword_matches[keyword_fields]

semantic_matches = pd.read_csv('match_results.csv')
semantic_fields = ['personID', 'firstname', 'name', 'paperID', 'title']
semantic_matches = semantic_matches[semantic_fields]
semantic_matches['reviewer_ID'] = semantic_matches['personID']
semantic_matches = semantic_matches.drop('personID', axis=1)
semantic_matches['reviewer_name'] = semantic_matches['name']
semantic_matches = semantic_matches.drop('name', axis=1)
semantic_matches['reviewer_firstname'] = semantic_matches['firstname']
semantic_matches = semantic_matches.drop('firstname', axis=1)

# check that the two dataframes have the same columns
assert all(keyword_matches.columns == semantic_matches.columns)

# where are the reviewer_ID and paperID columns the same?
# (i.e. where are the matches the same?)
merged_matches = pd.merge(keyword_matches, semantic_matches, on=['reviewer_ID', 'paperID'])
#40! matches, suggests 

