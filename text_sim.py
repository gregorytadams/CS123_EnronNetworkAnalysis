from gensim import corpora, similarities, models
from collections import defaultdict
from heapq import nlargest
import os
import logging
import numpy as np
import random

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stoplist = set('for a of the and or to in and as at from'.split())

def tokenize(fname):
    '''
    '''
    return [word for word in open(fname).read().lower().split() if (not word in stoplist)]

def build_dict(fnames):
    '''
    '''
    files_gen = (tokenize(f) for f in fnames)
    d = corpora.Dictionary(i for i in files_gen) 
    once_ids = [tokenid for tokenid, docfreq in d.dfs.items() if docfreq == 1]
    d.filter_tokens(once_ids)
    d.compactify()
    return d

def gen_files(path):
    '''
    '''
    for f in os.listdir(path):
        yield path + f

def gen_sample(path, n):
    '''
    '''
    return (path + x for _, x in nlargest(n, ((random.random(), f) for f in gen_files(path))))


class Comparitor():
    def __init__(self, train_fnames, test_fnames):
        '''
        '''
        self.train_fnames = train_fnames
        self.test_fnames = test_fnames
        self.d = build_dict([train_fnames])       
        
        corpora.MmCorpus.serialize('/tmp/corpus.mm', (v for v in self))
        self.corpus = corpora.MmCorpus('/tmp/corpus.mm')
        
        models.TfidfModel(self.corpus).save('/tmp/model.tfidf')
        self.corpus_tfidf = models.TfidfModel.load('/tmp/model.tfidf')[self.corpus]

        #models.RpModel(self.tfidf[self.corpus], num_topics=500).save('/tmp/model.rp')
        #self.corpus_rp = models.RpModel.load('/tmp/model.rp')[self.corpus_tfidf]
       
    def __iter__(self):
        '''
        '''
        for f in self.test_fnames:
            yield self.d.doc2bow(tokenize(f))

        
    

            
