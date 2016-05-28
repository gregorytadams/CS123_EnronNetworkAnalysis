from gensim import corpora, similarities, models
from collections import defaultdict
stoplist = set('for a of the and or to in and as at from'.split())

def tokenize(body):
    '''
    '''
    tokens = [word for word in body.lower().split() if not word in forbidden]
    counts = defaultdict(int)
    for word in tokens:
            counts[word] += 1
    return [word for word in tokens if counts[word] > 1]


def lsi(c, n):
    '''
    '''
    return models.LsiModel(c, n)

def tfidf(c):
    '''
    '''
    return models.TfidfModel(c)

class Corpus(object):
    def __init__(self, fnames):
        '''
        '''
        self.fnames = fnames
        self.dictionary = corpora.Dictionary(open(f).read().lower().split() for f in fnames) #iterable 
        stop_ids = [self.dictionary.token2id[stopword] for stopword in stoplist
                    if stopword in self.dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.items()
                    if docfreq == 1]
        self.dictionary.filter_tokens(stop_ids + once_ids)
        self.dictionary.compactify()

        
class Comparitor(corpus_fnames, compare_fnames):
    def __init__(self):
        '''
        '''
        self.corpus = Corpus(corpus_fnames)
        self.compare_fnames = compare_fnames
        self.model = model

    def __iter__(self):
        '''
        '''
        for f in self.compare_fnames:
            yield self.corpus.dictionary.doc2bow(open(f).read().lower().split())
            
        
     


            
