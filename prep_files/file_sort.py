import os
import sys

def sort_by_extension(list_of_extensions):
        # print("HERE I AM")
        os.mkdir('other2')
        for ext in list_of_extensions:
                os.mkdir(ext)
        for f in next(os.walk('.'))[2]:
                # print(f[-7:-4])
                # print(f[-7:-4] == 'pst' or f[-7:-4] == 'xml')
                # print([x[0] for x in os.walk('.')])
                if str('./' + f[-7:-4]) in [x[0] for x in os.walk('.')]:
                        print("Moving {} to {}".format(f, f[-7:-4]))
                        os.rename(f, f[-7:-4] + '/' + f)
                else:
                        os.rename(f, 'other2/' + f)

if __name__ == "__main__":
        os.chdir(sys.argv[1])
        print("Sorting Directory {}".format(sys.argv[1]))
        sort_by_extension(['pst', 'xml'])
