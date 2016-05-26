from gensim import corpora, similarities, models
from collections import defaultdict

forbidden = set(('for a of the and or to in and as at from' +\
                 'i you we he his her hers us them that yes no not').split())

def tokenize(body):
    '''
    '''
    tokens = [word for word in body.lower().split() if not word in forbidden]
    counts = defaultdict(int)
    for word in tokens:
            counts[word] += 1
    return [word for word in tokens if counts[word] > 1]
    
class Corpus(object):
    def __init__(self, current_fname, last_k_fnames):
        '''
        '''
        self.current_fname = current_fname
        self.last_k_fnames = last_k_fnames
        self.tokenized = tokenize(open(current_fname).read())
        self.dictionary = corpora.Dictionary([self.tokenized])
        corpora.MmCorpus.serialize('models/{}.mm'.format(current_fname.split('/')[-1]),
                                   [self.dictionary.doc2bow(self.tokenized)])
        self.corpus = corpora.MmCorpus('models/{}.mm'.format(current_fname.split('/')[-1]))
        self.lsi = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=2)
                
    def __iter__(self):
        '''
        '''
        for f in self.last_k_fnames:
            yield (f, self.lsi[self.dictionary.doc2bow(tokenize(open(f).read()))][0][1])
