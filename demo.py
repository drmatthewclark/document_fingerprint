from os import listdir
from os.path import isfile, join
from fp import fp
import pickle


def test():
   f = fp() 
   with open('sample.txt', 'r', encoding='utf-8') as file:
     text = file.read()
     f.processDoc(text)
     print('length %d density %5.4f bits set %d' % 
        (f.length, f.density(), f.countbits()) )
     
     g = fp()
     g.processDoc(text) 
     for i in range(20):
        g.fp_add(  'a'*i)

     print('length %d density %5.4f bits set %d' % 
        (g.length, g.density(), g.countbits()) )
     print('tanimoto %5.4f' % (f.tanimoto(g) ))

def test2():
    mypath='.'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    fprints = []
    count = 0
    for fe in onlyfiles:
       if not fe.endswith('txt'):
          continue

       with open(fe, mode='r', encoding='utf-8', errors='ignore') as f:
          count += 1
          text = f.read()
          fprint = fp()
          fprint.processDoc(text)
          fprints.append((fe, fprint))
          print(count, f.name, 'density', fprint.density())
    
    pickle.dump(fprints, open('pickles.pik', 'wb'))
    print('end')
       

test2() 
