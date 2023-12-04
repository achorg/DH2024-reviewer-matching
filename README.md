# DH2024-reviewer-matching

The [ADHO Conference Protocol](https://adho.org/conference/conference-protocol/) states that "PC chairs are responsible for determining the best algorithm for determining assignments of reviewers to submissions (e.g., via keyword)." 

Recent scholarship on the DH conference has noted the problems and limitations of keywords as a method of matching papers and reviewers. 

> "...the [ConfTool] algorithm does not accommodate submissions and reviewer expertise outside of the English language. ...While individually these issues can be resolved through creative solutions and human engineering, the underlying issue of the algorithm illustrates an English bias that undermines diversity efforts."[The circus we deserve? A front row look at the organization of the annual academic conference for the Digital Humanities](http://digitalhumanities.org:8081/dhq/vol/16/4/000643/000643.html) 

> "Things that might be taken for granted, such as keywords or subject areas, are actually powerful tools of inclusion and exclusion." [What gets categorized counts: Controlled vocabularies, digital affordances, and the international digital humanities conference](https://academic.oup.com/dsh/article/38/3/1088/6988912)

This project is an attempt to improve upon the current system by using multilingual text embeddings to match reviewers to papers.

### The algorithm is implemented in four scripts.
1. The first script `make_reviewers_csv.py` takes the reviewer data from ConfTool and adds information from Google and Google Scholar search in addition to the declared keywords. Search data was gathered with the Serp API so as to follow Google's terms of usage. The search query contains the reviewer's first and last name plus "digital humanities". The top results page and snippet text is saved, which provides greater context for matching. The script outputs a csv file called `reviewers.csv`.

2. The second script `reviewers_to_db.py` loads the data from reviewers.csv and adds it to a Chroma vector database.  The Language-agnostic BERT Sentence Embedding (LaBSE) model is used to create the embeddings. All text is chunked into blocks that can be processed by LaBSE.

3. The third script `make_matches.py` uses the vector database to match reviewers to papers based on similarity. All of the available information about a paper is used to make the match, including the title, abstract, and keywords. The papers are shuffled to avoid bias. For each paper, we look at the highest match. If the reviewer's max reviews is not met and there is less that three reviewers assigned to the paper, then an assignment is made. 

4. The fourth script `test_matches.py` is used to run tests of the final data and to assert that the matching algorithm is working as expected.

### Rationale of the algorithm:

- Approximates the processing of Googling a scholar and reviewing their publications as a human might do.
- Is meant to be a starting point and reference for the program committee, not an automated process. 
- The reviewer's declared keywords are used to create a vector for the reviewer. This is important for continuity with the previous reviewer matching system.
- Unlike ConfTool, a reviewer's instituional affliliation is not used to avoid conflict of interest. 


TODO:
Google Search -- bias of search engine, wrong match, results for multiple people with same name, etc.
Alternatives to "Google fingerprint?"

Test against real people, does it seem like a good match? 
Need to account for Language!! 
Add a requirements file  
