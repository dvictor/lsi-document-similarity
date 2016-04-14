#!/usr/bin/python

import gensim.corpora.wikicorpus as corpus
from db_connect import get_cursor

dbc = get_cursor()

'''
CREATE TABLE `wiki_pages` (
  `id` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` mediumtext NOT NULL,
  `is_artist` tinyint(1) NOT NULL,
  `size` int(11) NOT NULL
) DEFAULT CHARSET=utf8;

ALTER TABLE `wiki_pages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `is_artist` (`is_artist`),
  ADD KEY `size` (`size`),
  ADD KEY `title` (`title`);
'''

with open('enwiki-latest-pages-articles.xml') as fh:
    gen = corpus.extract_pages(fh)
    i = 0
    for title, text, pgid in gen:
        text = text.lower()
        if 'infobox musical artist' in text and ':' not in title:
            dbc.execute('INSERT INTO wiki_pages (id, title, content, is_artist) VALUES(%s, %s, %s, 1)',
                        [pgid, title, text])
            print i, title
            i += 1
