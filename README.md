# DH2024-reviewer-matching

Recent scholarship on the DH conference has noted problems with ConfTool's matching algorithm and its use of keywords for matching papers and reviewers. This system highly depends on the data reviewers provide when they register and authors when submitting their proposals. Entering many terms makes it possible to find a "strong" match with someone who has entered the same terms. However, this data is often lacking and open to interpretation and ambiguity. Keywords and topics are not reviewed or managed between conferences; they are exported from one ConfTool instance to another. Keywords are only available in English. As noted by several past conference organizers: 

> "...the [ConfTool] algorithm does not accommodate submissions and reviewer expertise outside of the English language. ...While individually these issues can be resolved through creative solutions and human engineering, the underlying issue of the algorithm illustrates an English bias that undermines diversity efforts." [The circus we deserve? A front row look at the organization of the annual academic conference for the Digital Humanities](http://digitalhumanities.org:8081/dhq/vol/16/4/000643/000643.html) 

The ConfTool algorithm cannot account for the similarity of topics. 

> "One author may select 'computer-assisted technology,' another 'machine learning,' still another 'artificial intelligence,' and a final one' natural language processing .' While we, as experts, know that these are all methodologically aligned, the [ConfTool] algorithm is unable to reconcile these terms together when it comes to assignment." [What gets categorized counts: Controlled vocabularies, digital affordances, and the international digital humanities conference](https://academic.oup.com/dsh/article/38/3/1088/6988912)

This project aims to improve on controlled-vocabulary-based matching by adding multilingual text embeddings to recommend matches between reviewers and papers. Embeddings are learned numerical representations of the meaning of text that are encoded by a large language model. 

![](https://1.bp.blogspot.com/-6upFrBNGwo4/Xzwk7D60GaI/AAAAAAAAGZs/ZDgmdCvBYfQr2cc5CkWW0AfIzD11x1q4wCLcBGAsYHQ/s0/image2%2B%25284%2529.jpg) 

Visualization of multilingual text embeddings from [Google AI Blog](https://ai.googleblog.com/2020/08/language-agnostic-bert-sentence.html)

### Goals of the algorithm:
- Address the English bias of the ConfTool algorithm by using multilingual text embeddings.
- Use the semantic similarity of topics to make matches between reviewers and papers in addition to exact keyword matches.

Sentence embeddings offer a more nuanced and contextual representation of the meaning of text than keywords. Keyword matching requires an exact match between the terms used by the reviewer and the terms used by the paper author. Embeddings allow for a more flexible match by using a distance score. Each match has a distance that can indicate similarity between the reviewer's described expertise and the paper description. 

Furthermore, sentence embeddings allow us to use a paper's title, abstract, and keywords to make a match. This is important because many papers do not have keywords. Many reviewers also do not have keywords, so we only have their names and institutions. To fill these gaps, we use information from the Index of Digital Humanities Conferences](https://dh-abstracts.library.virginia.edu/). 

For semantic search, it is important to compare similar kinds of texts. A reviewer's presentations at a DH conference provide a very comparable text that provides a meaningful distance score.  Given that scholars' interests and expertise are always changing, we also index reviewers' proposals to the current conference. 

The algorithm is implemented in Python and uses the [Language-agnostic BERT Sentence Embedding (LaBSE)](https://ai.googleblog.com/2020/08/language-agnostic-bert-sentence.html) model to create the embeddings. The LaBSE model was trained on 109 languages. 

### The algorithm is implemented in four scripts.
1. The first script `make_reviewers_csv.py` takes the reviewer data from ConfTool and adds information from the Index of Digital Humanities Conferences. The script outputs a csv file called `reviewers.csv`.

2. The second script `reviewers_to_db.py` loads the data from reviewers.csv and adds it to a [Chroma](https://docs.trychroma.com/) vector database. The Language-agnostic BERT Sentence Embedding (LaBSE) model is used to create the embeddings. All text is chunked into blocks that can be processed by LaBSE.

3. The third script `make_matches.py` uses the vector database to match reviewers to papers based on similarity. All of the available information about a paper is used to make the match, including the title, abstract, and keywords. The papers are shuffled to avoid bias during assignments. For each paper, we look at the highest match. If a reviewer has not reached their maximum number of reviews and the paper has less than three reviewers assigned, then an assignment is made. 

4. The fourth script, `test_matches.py,` is used to run tests of the final data and to assert that the matching algorithm is working as expected.

### Rationale of the algorithm:

- This algorithm is meant to be a starting point and reference for the program committee, not an automated process. 
- A reviewer's declared keywords are still key to the matching process, given that they can provide a 1:1 match with a paper's keywords. 
- The algorithm does not distinguish between presentation types. It is just as likely to assign a poster to a senior scholar as it is to assign a long paper to a graduate student. This choice invites further discussion and relflection. 
- The algorithm does not try to find potential conflicts of interest. "Conflicts of interest include collaborators, projects on which you have worked, colleagues at your institution, or a situation in which your evaluation (positive or negative) would be professionally advantageous to you" ([src](https://ach2023.ach.org/en/reviewer-guidelines/)). Conflict of interest identification can be done using ConfTool with a reviewer's name, email address, and institutional affiliation [(see)](https://www.conftool.net/ctforum/index.php/topic,117.0.html). As Jennifer Guiliano and Laura Estil note, "Given how common large, multi-institutional projects are, as well as collaborative work more generally in the digital humanities, the current automated conflict of interest process [in ConfTool] is insufficient." When a review is assigned, it is important to give the potential reviewer [the option to decline, given a potential conflict](https://www.conftool.net/ctforum/index.php/topic,229.0.html). 
