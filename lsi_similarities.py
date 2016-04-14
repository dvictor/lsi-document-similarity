#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Victor Dramba
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


import logging
import gensim
import pickle
import os.path as path

PREFIX = 'data/of3'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = gensim.corpora.Dictionary.load_from_text(PREFIX + '_wordids.txt.bz2')

# load corpus iterator
mm = gensim.corpora.MmCorpus(PREFIX + '_tfidf.mm')

print '\nTF-IDF corpus:'
print mm
print


def train_model():
    print '\nTraining LSI model'
    # extract 400 LSI topics; use the default one-pass algorithm
    m = gensim.models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=400)
    m.print_topics(10)
    m.save(PREFIX + '_lsi.bin')
    return m

if path.isfile(PREFIX + '_lsi.bin'):
    lsi = gensim.models.lsimodel.LsiModel.load(PREFIX + '_lsi.bin')
else:
    lsi = train_model()


def make_similarities():
    print '\nTraining similarities'
    idx = gensim.similarities.MatrixSimilarity(lsi[mm])
    idx.save(PREFIX + '_lsi_similarities.index')
    return idx

if path.isfile(PREFIX + '_lsi_similarities.index'):
    index = gensim.similarities.MatrixSimilarity.load(PREFIX + '_lsi_similarities.index')
else:
    index = make_similarities()

docindex = pickle.load(open(PREFIX + '_docindex.p', 'rb'))
id2title = dict(docindex)
pageid2pos = dict([(tup[0], i) for i, tup in enumerate(docindex)])


#5422144 taylor swift
#18313 louis armstrong
#28715 system of a down
#98369 Jethro Tull
#145995 creedence
docNo = pageid2pos['28715']
print docindex[docNo]

l = [id2word[wid] for wid, freq in mm[docNo]]
print ' '.join(l)

vec_lsi = lsi[mm[docNo]]
sims = index[vec_lsi]
ssims = sorted(enumerate(sims), key=lambda item: -item[1])
for i, (dno, score) in enumerate(ssims[:50]):
    pageid, title = docindex[dno]
    print '%s) %s - %s (%s%%)' % (i, title, pageid, int(score*100))


