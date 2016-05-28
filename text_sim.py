from gensim import corpora, similarities, models
from collections import defaultdict

stoplist = set('for a of the and or to in and as at from'.split())

class Dict(object):
    def __init__(self, fnames):
        '''
        '''
        self.fnames = fnames
        self.dict = corpora.Dictionary(open(f).read().lower().split() for f in fnames) #iterable 
        stop_ids = [self.dict.token2id[stopword] for stopword in stoplist
                    if stopword in self.dict.token2id]
        once_ids = [tokenid for tokenid, docfreq in self.dict.dfs.items()
                    if docfreq == 1]
        self.dict.filter_tokens(stop_ids + once_ids)
        self.dict.compactify()

        
class Comparitor():
    def __init__(self, corpus_fnames, compare_fnames, given_name = ''):
        '''
        '''
        self.Dict = Dict(corpus_fnames)
        self.compare_fnames = compare_fnames
        self.serialize('/tmp/corpus.mm')
        self.corpus = corpora.MmCorpus('/tmp/corpus.mm')
        
    def __iter__(self):
        '''
        '''
        for f in self.compare_fnames:
            yield self.Dict.dict.doc2bow(open(f).read().lower().split())

    def serialize(self):
        '''
        '''
        corpora.MmCorpus.serialize('/tmp/corpus.mm', v for v in self)
    
     


            
