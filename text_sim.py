from gensim import corpora, similarities, models
from collections import defaultdict
import heapq
import os
import sys
import logging
import random
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stopwords = set('for a of the and or to in and as at from this is with that be any all if'.split())

def tokenize(fname):
    '''
    '''
    words = []
    n = 0
    for line in open(fname):
        n += 1
        if n > 4:
            for word in line.lower().split():
                words.append(word)
    words = words[:-46]
    if len(words) > 0:
        return words
    
class Comparitor():
    def __init__(self, train_dir, test_dir, num_dims=200):
        '''
        '''
        self.train_dir = train_dir
        self.test_dir = test_dir
        print('\nBuilding dict\n{}'.format('~'*40))
        self.d = self.build_dict(train_dir) 
        print('\nBuilding corpus\n{}'.format('~'*40))
        corpora.MmCorpus.serialize('models/corpus.mm', (v for v in self))
        self.corpus = corpora.MmCorpus('models/corpus.mm')
        print('\nBuilding LSI model\n{}'.format('~'*40))
        models.LsiModel(self.corpus, id2word=self.d, num_topics=num_dims).save('models/model.lsi')
        self.lsi = models.LsiModel.load('models/model.lsi')
        print('\nBuilding similarity index\n{}'.format('~'*40))
        self.index = similarities.Similarity('models/lsi.index', self.lsi[self.corpus], self.corpus.num_terms)
        
    def __iter__(self):
        '''
        '''
        for f in self.gen_files(self.train_dir):
            yield self.d.doc2bow(tokenize(f))

    def sim_query(self):
        '''
        '''
        for f in self.gen_files(self.test_dir):
            yield (f, self.index[self.d.doc2bow(tokenize(f))].mean())

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
        
    def gen_files(self, path):
        '''
        '''
        for f in os.listdir(path):
            yield os.path.join(path, f)

    def gen_sample(self, path, n):
        '''
        '''
        return (x for _, x in heapq.nlargest(n, ((random.random(), f) for f in self.gen_files(path))))

    def build_dict(self, train_dir):
        '''
        '''
        files_gen = (tokenize(f) for f in self.gen_files(train_dir))
        d = corpora.Dictionary(i for i in files_gen) 
        once_ids = [tokenid for tokenid, docfreq in d.dfs.items() if docfreq == 1]
        d.filter_tokens(once_ids)
        d.compactify()
        return d
    
if __name__ == '__main__':
    args = sys.argv
    if len(args) == 6:
        c = Comparitor(args[1], args[2], num_dims = int(args[5]))
        top_k = sorted(c.top_k(int(sys.argv[4])), key=lambda tup: tup[1])[::-1]
        with open(args[3], 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for tup in top_k:
                writer.writerow(tup)   
    else:
        print('Usage: python3 <train_dir> <test_dir> <output_csv_fname> <k (top k)> <n (dimensions)>')
