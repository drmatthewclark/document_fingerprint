import pickle
from fp import fp
import math
from nltk.stem.snowball import SnowballStemmer
  

def read(fname):
    with open(fname, 'rb') as f:   
      array = pickle.load(f)

    return array


def nxn(fname):
    data =  read(fname)
    size = len(data)
    for i1 in range(size):
        name1, f1 = data[i1]
        print(',%s' % (name1), end='')
    print('')

    for i1 in range(size):
        name1, f1 = data[i1]
        print('%s' % (name1), end='')

        for i2 in range(size):
            (name2, f2)  = data[i2]
            similarity = f1.tanimoto(f2)
            if name1 == name2:
                print(',', end = '')
            else:
                print(',%5.3f' % (similarity), end='' )
        print('')
 
nxn('pickles.pik')
