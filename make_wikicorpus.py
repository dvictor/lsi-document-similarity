#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Radim Rehurek <radimrehurek@seznam.cz>
# Copyright (C) 2012 Lars Buitinck <larsmans@gmail.com>
# Copyright 2016 Victor Dramba
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


import logging
import os.path
import sys

from gensim.corpora import Dictionary, HashDictionary, MmCorpus
from gensim.models import TfidfModel
from wiki_corpus import WikiCorpus
import pickle

from db_connect import get_cursor


# Wiki is first scanned for all distinct word types (~7M). The types that
# appear in more than 10% of articles are removed and from the rest, the
# DEFAULT_DICT_SIZE most frequent types are kept.
DEFAULT_DICT_SIZE = 100000
OUT_PREFIX = 'data/of3'


def pages_gen():
    dbc = get_cursor()

    dbc.execute('SELECT id, title, content FROM wiki_pages WHERE is_artist=1 ORDER BY id')
    for pageid, title, content in dbc:
        yield pageid, title, content


def main():
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    outp = OUT_PREFIX
    keep_words = DEFAULT_DICT_SIZE

    # the doc index
    dbc = get_cursor()
    dbc.execute('SELECT id, title FROM wiki_pages WHERE is_artist=1 ORDER BY id')
    docindex = [(pageid, title) for pageid, title in dbc]
    pickle.dump(docindex, open(outp + '_docindex.p', 'wb'))

    lemmatize = True  # 'lemma' in program

    wiki = WikiCorpus(pages_gen, lemmatize=lemmatize)
    # only keep the most frequent words
    wiki.dictionary.filter_extremes(no_below=20, no_above=0.5, keep_n=DEFAULT_DICT_SIZE)
    # save dictionary and bag-of-words (term-document frequency matrix)
    MmCorpus.serialize(outp + '_bow.mm', wiki, progress_cnt=10000)
    wiki.dictionary.save_as_text(outp + '_wordids.txt.bz2')
    dictionary = Dictionary.load_from_text(outp + '_wordids.txt.bz2')

    # initialize corpus reader and word->id mapping
    mm = MmCorpus(outp + '_bow.mm')

    # build tfidf, ~50min
    tfidf = TfidfModel(mm, id2word=dictionary, normalize=True)
    tfidf.save(outp + '.tfidf_model')

    # save tfidf vectors in matrix market format
    # another long task
    MmCorpus.serialize(outp + '_tfidf.mm', tfidf[mm], progress_cnt=10000)

    logger.info("finished running %s" % program)

if __name__ == '__main__':
    main()
