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
    def __init__(self, train_fnames='', test_fnames='', num_topics=200):
        '''
        '''
        self._train_fnames = train_fnames
        self._test_fnames = test_fnames
        print('Building dict\n{}'.format('~'*40))
        self.d = build_dict(train_fnames)       
        print('Building corpus\n{}'.format('-'*20))
        corpora.MmCorpus.serialize('models/corpus.mm', (v for v in self))
        self.corpus = corpora.MmCorpus('models/corpus.mm')
        print('Building LSI model\n{}'.format('-'*20))
        models.LsiModel(self.corpus, id2word=self.d, num_topics=num_topics).save('models/model.lsi')
        self.lsi = models.LsiModel.load('models/model.lsi')
        print('Building similarity index\n{}'.format('-'*20))
        self.index = similarities.Similarity('models/lsi.index', self.lsi[self.corpus], self.corpus.num_terms)
        
    def __iter__(self):
        '''
        '''
        for f in self._train_fnames:
            yield self.d.doc2bow(tokenize(f))

    def sim_query(self):
        '''
        '''
        for f in self._test_fnames:
            yield self.index[self.d.doc2bow(tokenize(f))].mean()
                    

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 3:
        c = Comparitor(gen_files(args[1]), gen_files(args[2]))
    else:
        print('Usage: python3 <train_dir> <test_dir>')
