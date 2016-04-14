
Find similar documents using LSI and cosine similarity matrix
=============================================================


This program finds similar documents the one provided as a query.
It can be used to build a recommendation system, automation
of knowledgebase systems etc.


Latent Semantic Indexing (LSI) builds on the assumption that words that are used in the same
contexts tend to have similar meanings. It can extract the conceptual content of a body of text
by establishing associations between terms that occur in similar contexts.


### Run

The preparing tasks can take many hours, depending on your computer capabilities.

 - download a Wikipedia archive, enwiki-latest-pages-articles.xml.bz2 ~13GB
 - create your database, see `db_connect.py`
 - run `db-import-music-pages.py`
 - run `make_wikicorpus.py` to prepare the corpus
 - run `lsi_similarities` to get similarities for a document
 
At the first run, `lsi_similarities.py` creates the index and saves it to disk.  
Next runs will load the saved index.
