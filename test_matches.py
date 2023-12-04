import pandas as pd 

reviewers = pd.read_csv('reviewers.csv')
matches = pd.read_csv('match_results.csv')

# Assert that each paper in matches has 3 reviewers
assert matches.groupby('paperID').count().max()[0] == 3

# Assert that no reviewer has more than max_reviews 

# Assert that no reviewer is assigned to the same paper more than once 


