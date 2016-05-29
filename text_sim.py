from gensim import corpora, similarities, models
from collections import defaultdict
import heapq
import os
import sys
import logging
import random
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stopwords = set(('for a of the and or to in and as at from this is with that be any all if'+\
                 'x-sdoc: i ').split())

def tokenize(fname):
    '''
    '''
    words = []
    n = 0
    for line in open(fname):
        n += 1
        if n > 6:
            for word in line.lower().split():
                words.append(word)
    return words[:-50]
    
def gen_files(path, n=None):
    '''
    '''
    for f in os.listdir(path)[:n]:
        yield os.path.join(path, f)

def gen_tokens(path, n=None):
    '''
    '''
    for f in gen_files(path, n):
        t = tokenize(f)
        if len(t) > 0:
            yield (f, t)
            
def build_dict(path, n=None):
    '''
    '''
    tokens_gen = (t for _, t in gen_tokens(path, n))
    d = corpora.Dictionary(i for i in tokens_gen) 
    once_ids = [tokenid for tokenid, docfreq in d.dfs.items() if docfreq == 1]
    d.filter_tokens(once_ids)
    d.compactify()
    return d

class Comparitor():
    def __init__(self, path, n_dims=200):
        '''
        '''
        self.n_train_files = 1000
        self.path = path
        print('\nBuilding dict\n{}'.format('~'*40))
        self.d = build_dict(path, n=self.n_train_files) 
        print('\nBuilding corpus\n{}'.format('~'*40))
        corpora.MmCorpus.serialize('models/corpus.mm', (v for _, v in self))
        self.corpus = corpora.MmCorpus('models/corpus.mm')
        print('\nBuilding LSI model\n{}'.format('~'*40))
        models.LsiModel(self.corpus, id2word=self.d, num_topics=n_dims).save('models/model.lsi')
        self.lsi = models.LsiModel.load('models/model.lsi')
        print('\nBuilding similarity index\n{}'.format('~'*40))
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus], num_features = self.corpus.num_terms)
        
    def __iter__(self):
        '''
        '''
        for f, t in gen_tokens(self.path, self.n_train_files):
            yield (f, self.d.doc2bow(t))

    def sim_query(self):
        '''
        '''
        for f, t in gen_tokens(self.path):
            yield (f, self.index[self.d.doc2bow(t)].mean())

    def top_k(self, k):
        '''
        '''
        l = [('', 0)] * k
        heapq.heapify(l)
        for fname, score in self.sim_query():
            min_name, min_score = l[0]
            if score > min_score:
                heapq.heapreplace(l, (fname, score))
        return l        
    
if __name__ == '__main__':
    args = sys.argv
    if len(args) == 5:
        c = Comparitor(args[1], n_dims = int(args[4]))
        print('\nFinding top {} similarities\n{}'.format(args[3], '~'*40))
        top_k = sorted(c.top_k(int(sys.argv[3])), key=lambda tup: tup[1])[::-1]
        print('\nWriting top {} similarities to "{}"\n{}'.format(args[3], args[2], '~'*40))
        with open(args[2], 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for tup in top_k:
                writer.writerow(tup)   
    else:
        print('Usage: python3 <path> <output_csv_fname> <k (top k)> <n (dimensions)>')
