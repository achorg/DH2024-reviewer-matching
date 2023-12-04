# DH2024-reviewer-matching


This is a set of scripts to match reviewers to papers for the DH2024 conference. 

1. The first script `make_reviewers_csv.py` takes the reviewer data from ConfTool and adds information from Google search in addition to the declared keywords. The search contains the reviewer's first and last name plus "digital humanities". The script outputs a csv file called `reviewers.csv`.

2. The second script `reviewers_to_db.py` loads the data from reviewers.csv and adds it to a Chroma vector database.  The language agnostic BERT sentence transformer (LaBSE) is used to create the embeddings. All text is chunked into blocks that can be processed by LaBSE.

3. The third script `make_matches.py` uses the vector database to match reviewers to papers based on similarity. All of the available information about a paper is used to make the match, including the title, abstract, and keywords. The papers are shuffled to avoid bias. For each paper, we look at the highest match. If the reviewer's max reviews is not met and there is less that three reviewers assigned to the paper, then an assignment is made. 

