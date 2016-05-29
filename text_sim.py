from gensim import corpora, similarities, models
from collections import defaultdict
from heapq import nlargest
import os
import sys
import logging
import numpy as np
import random

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stopwords = set('for a of the and or to in and as at from'.split())

def tokenize(fname):
    '''
    '''
    return [word for word in open(fname).read().lower().split() if not word in stopwords]

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
        yield os.path.join(path, f)

def gen_sample(path, n):
    '''
    '''
    return (x for _, x in nlargest(n, ((random.random(), f) for f in gen_files(path))))


class Comparitor():
    def __init__(self, train_fnames, test_fnames):
        '''
        '''
        self.train_fnames = train_fnames
        self.test_fnames = test_fnames
        print('Building dict\n{}'.format('~'*40))
        self.d = build_dict(train_fnames)       
        print('Building corpus\n{}'.format('-'*20))
        corpora.MmCorpus.serialize('/tmp/corpus.mm', (v for v in self))
        self.corpus = corpora.MmCorpus('/tmp/corpus.mm')
        print('Building tfidf scores\n{}'.format('-'*20))
        models.TfidfModel(self.corpus).save('/tmp/model.tfidf')
        self.tfidf = models.TfidfModel.load('/tmp/model.tfidf')[self.corpus]
        
    def __iter__(self):
        '''
        '''
        for f in self.test_fnames:
            yield self.d.doc2bow(tokenize(f))

if __name__ == '__main__':
    args = sys.argv()
    if len(args) == 3:
        c = Comparitor(gen_files('text_001'), gen_files('all_text'))
