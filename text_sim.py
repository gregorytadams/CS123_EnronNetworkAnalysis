from gensim import corpora, similarities, models
from collections import defaultdict
import os

stoplist = set('for a of the and or to in and as at from'.split())

class Dict(object):
    def __init__(self, fnames):
        '''
        '''
        self.fnames = fnames
        self.d = corpora.Dictionary(open(f).read().lower().split() for f in fnames) #generator 
        stop_ids = [self.d.token2id[stopword] for stopword in stoplist
                    if stopword in self.d.token2id]
        once_ids = [tokenid for tokenid, docfreq in self.d.dfs.items()
                    if docfreq == 1]
        self.d.filter_tokens(stop_ids + once_ids)
        self.d.compactify()
     
class Comparitor():
    def __init__(self, fnames):
        '''
        '''
        self.fnames = fnames
        self.D = Dict(fnames)
        self._serialize()
        self.corpus = corpora.MmCorpus('/tmp/corpus.mm')
        self.tfidf = models.TfidfModel(self.corpus)[self.corpus]
        
    def __iter__(self):
        '''
        '''
        for f in self.fnames:
            yield self.D.d.doc2bow(open(f).read().lower().split())

    def _serialize(self):
        '''
        '''
        corpora.MmCorpus.serialize('/tmp/corpus.mm', (v for v in self)) #generator
    
    

            
