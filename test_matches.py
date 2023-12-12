import pandas as pd 

reviewers = pd.read_csv('reviewers.csv')
matches = pd.read_csv('match_results.csv')
papers = pd.read_csv('DH2024WashingtonDC_papers_2023-12-11_04-33-28.csv')

# Sufficient reviewer capacity (reviewer sum max reviews > num reviews needed)
reviewers_matches = reviewers.merge(matches, on='personID')
reviewers_matches['maxreviews'].sum() >= len(papers) * 4
print(f"Reviewer pool capacity is {int(reviewers['maxreviews'].sum())} reviews. {len(papers) * 4} are needed.")

# Match threshold 
print("Lowest match distance " + str(matches['distance'].min()))
print("Highest match distance: " + str(matches['distance'].max()))

# Assert that each paper in matches has 3 reviewers
assert matches.groupby('paperID').count().max()[0] >= 3, "Each paper should have 3 reviewers"

# Assert no duplicate titles. Suggests multiple submissions of the same paper with different id 
#  len(papers['title'].unique()) == len(papers), "No duplicate titles"

# Assert that no reviewer has more than max_reviews 
reviewers_matches = reviewers.merge(matches, on='personID')
assert reviewers_matches.groupby('personID').count().max()[0] <= reviewers_matches.groupby('personID').max()['maxreviews'].max(), "No reviewer should have more than max_reviews"

# Assert that no reviewer is assigned to the same paper more than once 
assert reviewers_matches.groupby(['personID','paperID']).count().max()[0] == 1, "No reviewer should be assigned to the same paper more than once"

# No author is assigned to review their own paper
papers_matches = papers.merge(matches, on='paperID')
papers_matches['reviewer_name'] = papers_matches['name'] + ", " + papers_matches['firstname']
papers_matches['is_author'] = papers_matches.apply(lambda row: row['reviewer_name'] in row['authors'], axis=1)
assert papers_matches['is_author'].sum() == 0, "No author should be assigned to review their own paper"

print("All Tests Passed!")
