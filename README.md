# DH2024-reviewer-matching


This is a set of scripts to match reviewers to papers for the DH2024 conference. 

1. The first script `make_reviewers_csv.py` takes the reviewer data from ConfTool and adds information from Google and Google Scholar search in addition to the declared keywords. Search data was gathered with the Serp API so as to follow Google's terms of usage. The search query contains the reviewer's first and last name plus "digital humanities". The top results page and snippet text is saved, which provides greater context for matching. The script outputs a csv file called `reviewers.csv`.

2. The second script `reviewers_to_db.py` loads the data from reviewers.csv and adds it to a Chroma vector database.  The language agnostic BERT sentence transformer (LaBSE) is used to create the embeddings. All text is chunked into blocks that can be processed by LaBSE.

3. The third script `make_matches.py` uses the vector database to match reviewers to papers based on similarity. All of the available information about a paper is used to make the match, including the title, abstract, and keywords. The papers are shuffled to avoid bias. For each paper, we look at the highest match. If the reviewer's max reviews is not met and there is less that three reviewers assigned to the paper, then an assignment is made. 

Rationale for the matching algorithm:


The circus we deserve? A front row look at the organization of the annual academic conference for the Digital Humanities 
http://digitalhumanities.org:8081/dhq/vol/16/4/000643/000643.html

What gets categorized counts: Controlled vocabularies, digital affordances, and the international digital humanities conference https://academic.oup.com/dsh/article/38/3/1088/6988912

Google Search -- bias of search engine, wrong match, results for multiple people with same name, etc.
Alternatives to "Google fingerprint?"

Test against real people, does it seem like a good match?