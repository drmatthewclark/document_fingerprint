import hashlib
import re
import math
import nltk
import pickle
from nltk.stem.snowball import SnowballStemmer

class fp:

   length = 8096     # length of fingerprint, in bits (highest bit is length-1)
   bits_per_text = 1  # number of bits to set for each text fragment
   min_word_length = 2 # words shorter than this omitted
   max_word_length = 25 # words longer than this omitted
   ngrams = [1]  # ngrams to process
   language='english'  # language for stemming
   stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'aren', "didnt", "doesnt",  'haven', "shouldnt",  'would']

   encoding = 'utf-8'  # encoding

   def __init__(self, value = 0):
      self.fprint = 0
      self.stemmer = SnowballStemmer(fp.language)
      self.length = fp.length


   def __str__(self):
      return self.str()

   def half(self):
      """ folds the integer in half to reduce size """
      bits = self.length 
      half = int(bits/2)
      mask = 2**(half+1) - 1
      first = self.fprint >> half
      self.fprint = (first ^ self.fprint) & mask
      self.length = half

   def _hash(self, string):
      """ return an array with bits to set for the string
          the array size is set by bits_per_text
      """
      result = []
      val = hashlib.md5(string.encode(fp.encoding)).hexdigest()
      num = int(val, 16)
      for i in range(fp.bits_per_text):
         result.append( (num & 0xFFFF) % self.length )
         num >>= 16

      return result

   def str(self):
      """ convert the fingerprint to string for printing """
      result = ''
      t = self.fprint
      while(t):
         result += str(t&1)
         t >>= 1
      
      return result

   def set(self, bit):
      """ set a bit in the fingerprint by value
          bit can be a sparse array (list of bits) or a
          single bit
      """
      if type(bit) == list:
         for val in bit:
            num = 1<< val 
            self.fprint |= num
      else:   
         num = 1<<bit
         self.fprint |= num


   def _process(self, text, step):
      """ split the text into ngrams of with 'step' words per chunk 
          set the fprint bits for each text 
      """
      words = self.preprocess(text)
      lw = len(words)
      if lw < step:
         pass

      for i in range(0, lw - step, step):
         w = ' '.join(words[i:i+step])
         if  w.count(' ') == step - 1:
           self.fp_add(w)


   def fp_add(self, text):
      """ set the bits computed for the given text string """
      self.set(self._hash(text))


   def preprocess(self, text):
      """ preprocess the text to remove non-characters, 
          split into individual words
          stem each word with the chosen stemmer/language
      """
      text = text.lower()
      text = re.sub('[^a-z\s]', '', text)
      text = re.sub('\s+', ' ', text)
      words = text.split()
      result = []

      for w in words:
         w = self.stemmer.stem(w)
         if len(w) >= fp.min_word_length and len(w) < fp.max_word_length and w not in fp.stopwords:
            result.append(w)

      return result


   def processDoc(self, text):
      """ process an entire document into this fingerprint 
          using the chosen stemmer, number of bits and 
          number of ngrams etc. 
      """
      for n in fp.ngrams:
         self._process(text, n)
      
   def get(self):
      """ get the fingerprint integer for this fingerprint """
      return int(self.fprint)

   def density(self):
      """ return the bit density of this fingerprint """
      return self._countbits(self.fprint)/self.length

   def countbits(self):
      """ return the number of set bits in this fingerprint """
      return self._countbits(self.fprint)

   def _countbits(self, t):
      """ return the number of set bits in this fingerprint """
      count = 0
      while(t):
         count += t & 1
         t >>= 1
      return count

   def tanimoto(self, f2):
      """ compute the tanimoto similarity between this and fingerprint f2 """
      if self.length == f2.length:
         num = self._countbits(f2.get() & self.fprint)
         den = self._countbits(f2.get() | self.fprint)
         return num/den
      else:
         return 0.0

