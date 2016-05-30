# This is a script to uniformly bucket files in a directory.  

import os

def grab_files(n):
        '''
        Uniromly samples/buckets the text files.

        input: number of buckets
        '''
        for i in range(n):
                os.mkdir('files' + str(i))
        for i, f in enumerate(next(os.walk('.'))[2]):
                d_ext = i % n
                d = 'files' + str(d_ext)
                os.rename(f, d + '/' + f)

if __name__ == "__main__":
        grab_files(30)
