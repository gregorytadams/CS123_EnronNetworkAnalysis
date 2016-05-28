from gensim import corpora, similarities, models
from collections import defaultdict
import os
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stoplist = set('for a of the and or to in and as at from'.split())

class Dict(object):
    def __init__(self, fnames):
        '''
        '''
        self.fnames = fnames
        self.d = corpora.Dictionary(open(f).read().lower().split() for f in fnames)
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
        
        corpora.MmCorpus.serialize('/tmp/corpus.mm', (v for v in self))
        self.corpus = corpora.MmCorpus('/tmp/corpus.mm')
        
        models.TfidfModel(self.corpus).save('/tmp/model.tfidf')
        self.tfidf = models.TfidfModel.load('/tmp/model.tfidf')

        models.rpmodel.RpModel(self.tfidf, num_topics=500).save('/tmp/model.rp')
        self.rp = models.rpmodel.RpModel.load('/tmp/model.rp')
        
        
    def __iter__(self):
        '''
        '''
        for f in self.fnames:
            yield self.D.d.doc2bow(open(f).read().lower().split())

    
        

        
    

            
