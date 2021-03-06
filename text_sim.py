from gensim import corpora, similarities, models
from collections import defaultdict
from optparse import OptionParser
import heapq
import os
import sys
import logging
import random
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stopwords = set(('for a of the and or to in and as at from this is with that be any all if'+\
                 'x-sdoc: i').split())

def tokenize(fname):
    '''
    Takes a file and reduces it to a list of "tokens": strings not forbidden by the set of 
    stopwords that fall within the approximate bounds of the email body (excluding the pre-
    and postscript). 
    '''
    words = []
    n = 0
    for line in open(fname):
        n += 1
        if n > 6:
            for word in line.lower().split():
                words.append(word)
    return words[:-50]
    
def gen_files(path, n, seed):
    '''
    Generates filenames in a given path (don't want to just use os.listdir, due to memory
    constraints). If n is not None, generates an n-length pseudorandom sample of the files.
    '''
    if n is None:
        for f in os.listdir(path):
            yield os.path.join(path, f)
    else:
        random.seed(seed)
        for f in random.sample(os.listdir(path), n):
            yield os.path.join(path, f)

def gen_tokens(path, n=None, seed=666):
    '''
    Calls tokenize() on a gen_files() generator, and yields a (file, tokens) tuple only if 
    there are more than zero valid tokens.
    '''
    for f in gen_files(path, n, seed):
        t = tokenize(f)
        if len(t) > 0:
            yield (f, t)
            
def build_dict(path, n=None, seed=666):
    '''
    Calls gen_tokens() on a given path, and indexes the tokens into a gensim dictionary. Then, 
    removes tokens that only occur once, and rehashes the entries in order to save memory.
    '''
    tokens_gen = (t for _, t in gen_tokens(path, n, seed))
    d = corpora.Dictionary(i for i in tokens_gen) 
    once_ids = [tokenid for tokenid, docfreq in d.dfs.items() if docfreq == 1]
    d.filter_tokens(once_ids)
    d.compactify()
    return d

class Comparitor():
    def __init__(self, path, out_fname, n_dims=200, n_train_files=1000, seed=666):
        '''
        Generates a "Latent Semantic Indexing" model based on a corpus of tokens from a 
        pseudorandom sample of files in the given path. Doesn't load them all into memory
        at once - uses an __iter__ block to process files one by one. The LSI model is a 
        decomposition of the space of all tokens into an "n_dims"-dimensional space.
        '''
        self.path = path
        self.out_fname = out_fname
        out_fname_stripped = out_fname.split('.')[-2].split('/')[-1]
        self.n_dims = n_dims
        self.n_train_files = n_train_files
        self.seed = seed
        
        print('\nBuilding dict\n{}'.format('~'*40))
        self.d = build_dict(path, n=self.n_train_files, seed=seed)
        print('\nBuilding corpus\n{}'.format('~'*40))
        corpora.MmCorpus.serialize('models/{}_corpus.mm'.format(out_fname_stripped),
                                   (v for _, v in self))
        self.corpus = corpora.MmCorpus('models/{}_corpus.mm'.format(out_fname_stripped))
        print('\nBuilding LSI model\n{}'.format('~'*40))
        models.LsiModel(self.corpus, id2word=self.d, num_topics=n_dims)\
              .save('models/{}_model.lsi'.format(out_fname_stripped))
        self.lsi = models.LsiModel.load('models/{}_model.lsi'.format(out_fname_stripped))
        print('\nBuilding similarity index\n{}'.format('~'*40))
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus],
                                                   num_features = self.corpus.num_terms)
        
    def __iter__(self):
        '''
        Iterates over a pseudorandom sampling of files in the given directory - yields
        (filename, bag_of_words) tuples for each file in the sample with more than zero 
        valid tokens.
        '''
        for f, t in gen_tokens(self.path, self.n_train_files, self.seed):
            yield (f, self.d.doc2bow(t))

    def sim_query(self):
        '''
        Iterates over all files in the given directory to calculate the mean cosine similarity of 
        a bag of words to the LSI model. Yields (filename, score) tuples for each file with more 
        than zero valid tokens.
        '''
        for f, t in gen_tokens(self.path):
            yield (f, self.index[self.d.doc2bow(t)].mean())

    def top_k(self, k, save=True):
        '''
        Returns a heap of the top-k scores for a sim_query() in a directory. 
        '''
        l = [('', 0)] * k
        heapq.heapify(l)
        n = 0
        for fname, score in self.sim_query():
            if n%1000 == 0:
                print('Processed {} entries'.format(n))
            n += 1
            min_name, min_score = l[0]
            if score > min_score:
                heapq.heapreplace(l, (fname, score))
        l = sorted(l, key=lambda tup: tup[1])[::-1]
        if save:
            with open(self.out_fname, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for tup in l:
                    writer.writerow(tup)   
        return l        
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--path', dest='path', help='Directory to analyze', default=None)
    parser.add_option('-o', '--outf', dest='outf', help='Output csv filepath', default=None)
    parser.add_option('-k', '--topk', dest='topk', help='Size of top-k heap', default=100)
    parser.add_option('-n', '--ndims', dest='ndims', help='Dimensionality of LSI model', default=200)
    parser.add_option('-t', '--train', dest='train', help='Number of training sample files', default=1000)
    parser.add_option('-s', '--seed', dest='seed', help='Seed for training data sample', default=666)
    o, _ = parser.parse_args()
    c = Comparitor(o.path, o.outf, o.ndims, o.train, o.seed)
    c.top_k(o.topk, save=True)
    
