# DH2024-reviewer-matching

The [ADHO Conference Protocol](https://adho.org/conference/conference-protocol/) states that "PC chairs are responsible for determining the best algorithm for determining assignments of reviewers to submissions (e.g., via keyword)." 

Recent scholarship on the DH conference has noted the problems and limitations of keywords, topics and terms as a method of matching papers and reviewers. Keywords and topics are not reviewed or managed between conferences, they are exported from one ConfTool instance to another. Topics are only available in English. 

> "...the [ConfTool] algorithm does not accommodate submissions and reviewer expertise outside of the English language. ...While individually these issues can be resolved through creative solutions and human engineering, the underlying issue of the algorithm illustrates an English bias that undermines diversity efforts."[The circus we deserve? A front row look at the organization of the annual academic conference for the Digital Humanities](http://digitalhumanities.org:8081/dhq/vol/16/4/000643/000643.html) 

Finally, the ConfTool algorithm is unable to account for the similarity of topics. 

> " One author may select ‘computer-assisted technology’, another ‘machine learning’, still another ‘artificial intelligence’, and a final one ‘natural language processing’. While we, as experts, know that these are all methodologically aligned, the [ConfTool] algorithm is unable to reconcile these terms together when it comes to assignment." [What gets categorized counts: Controlled vocabularies, digital affordances, and the international digital humanities conference](https://academic.oup.com/dsh/article/38/3/1088/6988912)

This project is an effort to improve upon controlled-vocabulary-based matching by using multilingual text embeddings to recommend matches between reviewers and papers. Sentence embeddings offer a more nuanced and contextual representation of the meaning of text than keywords. Keyword matching requires an exact match between the terms used by the reviewer and the terms used by the paper author. Embeddings allow for a more flexible match. Each match has a distance that can indicate similarity between the reviewer's described expertise and the paper description. 

Furthermore, sentence embeddings allow us to use a paper's title, abstract, and keywords to make a match. This is important because many papers do not have keywords. Many reviewers also do not have keywords, so we only have their name and institution. This information can be used to search for information about the reviewer using Google and Google Scholar.  

The algorithm is implemented in Python and uses the [Language-agnostic BERT Sentence Embedding (LaBSE)](https://ai.googleblog.com/2020/08/language-agnostic-bert-sentence.html) model to create the embeddings. The LaBSE model was trained on 109 languages and is available in 32 languages. 

### The algorithm is implemented in four scripts.
1. The first script `make_reviewers_csv.py` takes the reviewer data from ConfTool and adds information from Google and Google Scholar search in addition to the declared keywords. Search data was gathered with the Serp API so as to follow Google's terms of usage. The search query contains the reviewer's first and last name plus "digital humanities". The top results title and snippet text is saved, which provides greater context for matching. The script outputs a csv file called `reviewers.csv`.

2. The second script `reviewers_to_db.py` loads the data from reviewers.csv and adds it to a [Chroma](https://docs.trychroma.com/) vector database.  The Language-agnostic BERT Sentence Embedding (LaBSE) model is used to create the embeddings. All text is chunked into blocks that can be processed by LaBSE.

3. The third script `make_matches.py` uses the vector database to match reviewers to papers based on similarity. All of the available information about a paper is used to make the match, including the title, abstract, and keywords. The papers are shuffled to avoid bias. For each paper, we look at the highest match. If the reviewer's max reviews is not met and there is less that three reviewers assigned to the paper, then an assignment is made. 

4. The fourth script `test_matches.py` is used to run tests of the final data and to assert that the matching algorithm is working as expected.

### Rationale of the algorithm:

- Is meant to be a starting point and reference for the program committee, not an automated process. 
- Approximates the processing of Googling a scholar and reviewing their publications as a human might do.
- The reviewer's declared keywords are used to create a vector for the reviewer. 
- Unlike ConfTool, a reviewer's instituional affliliation is not used to avoid conflict of interest. 

