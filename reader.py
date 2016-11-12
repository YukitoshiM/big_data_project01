# This program reads crowled Tweeter data
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import re
import sys
import MeCab as Mecab
from collections import defaultdict
import math

# class for reading Tweeter data for any given file 
class TweetReader():
   def __init__(self):
      self.tagger = Mecab.Tagger('-Ochasen')
      self.alnum_Reg = re.compile(r'^[a-zA-Z0-9_(:;,./?*+&%#!<>|\u3000)~=]+$')
      # These list prepared for data in the Tweeter, 
      # First 4 variables prepared for a line which is devided by tab space
      # Last 3 are for contexts that is devided by space
      # rt_flags: contains if the tweet is retweet or not
      # reps:     contains for whom the tweet was replied 
      # texts:    contains actual tweet message
      self.ids, self.dates, self.contexts, self.unk_nums, self.rt_flags = [], [], [], [], []
      self.reps, self.texts, self.lines, self.morpho= [], [], [], []
      self.noun_count, self.adj_count, self.verb_count = defaultdict(int), defaultdict(int), defaultdict(int)
      self.word_count = defaultdict(int)
      self.total_noun, self.total_adj, self.total_verb = 0, 0, 0
      self.total_words = 0

   # This method read lines in the input file and store it into class variable called self.lines
   def read_lines(self, filename):
      with open(filename, 'r') as f:
         self.lines = f.readlines()
      for i, line in enumerate(self.lines):
         if line == '\n':
            self.lines.pop(i)

   # This method get ids in self.lines and store it into class variable called self.ids
   def getIDs(self):
      for line in self.lines:
         temp_split = line.split('\t')
         if len(temp_split) == 1:
            self.ids.append( None )
         elif len(temp_split) == 2:
            self.ids.append( None )
         elif len(temp_split) == 3:
            self.ids.append( temp_split[0] )
         elif len(temp_split) == 4:
            self.ids.append( temp_split[0] )

   # This method get date info. in self.lines and store it into class variable called self.dates
   def getDates(self):
      for line in self.lines:
         temp_split = line.split('\t')
         if len(temp_split) == 1:
            self.dates.append( None )
         elif len(temp_split) == 2:
            self.dates.append( None )
         elif len(temp_split) == 3:
            self.dates.append( temp_split[1] )
         elif len(temp_split) == 4:
            self.dates.append( temp_split[1] )

   # This method get contexts info. in self.lines and store it into class variable called self.contexts
   def getContexts(self):
      for line in self.lines:
         temp_split = line.split('\t')
         if len(temp_split) == 1:
            self.contexts.append( temp_split[0] )
         elif len(temp_split) == 2:
            self.contexts.append( temp_split[0] )
         elif len(temp_split) == 3:
            self.contexts.append( temp_split[2] )
         elif len(temp_split) == 4:
            self.contexts.append( temp_split[2])
      # Since tweet message contains RT, @{name}, & actual message, messages are devided
      for context in self.contexts:
         # 1st case: contains 'RT' & @{name} & actual message
         # 2nd case: contains @{name} & actual message
         # 3rd case: contains only actual message
         if context[0:2] == 'RT':
            context = context.split()
            self.rt_flags.append(1)
            # Some message has 'RT' at the beggining of contex, but message is something like 'RT>fdsafsdf'
            # so this will be ignored! 
            try:
               self.reps.append(context[1])
               self.texts.append(self.emoji_eliminator(''.join(context[2:])))
            except:
               self.rt_flags.append(0)
               self.reps.append(None)
               self.texts.append(None)
               continue
         elif context[0] == '@':
            context = context.split()
            self.rt_flags.append(0)
            self.reps.append(context[0])
            self.texts.append(self.emoji_eliminator(''.join(context[1:])))
         else:
            self.rt_flags.append(0)
            self.reps.append(None)
            self.texts.append(self.emoji_eliminator(context))

   def emoji_eliminator(self, text):
      delList = []
      for i, c in enumerate(text):
         if c.encode('utf-8')[0] == 226 or c.encode('utf-8')[0] == 240 or self.isalnum_(c):
            delList.append(i)
      text = list(text)
      for i in reversed(delList):
         text.pop(i)
      return(''.join(text))

   def getUnkNums(self):
      for line in self.lines:
         temp_split = line.split('\t')
         if len(temp_split) == 1:
            self.unk_nums.append( None )
         elif len(temp_split) == 2:
            self.unk_nums.append( temp_split[1] )
         elif len(temp_split) == 3:
            self.unk_nums.append( None )
         elif len(temp_split) == 4:
            self.unk_nums.append( temp_split[3] )

   def isalnum_(self, s):
       return self.alnum_Reg.match(s) is not None


   def word_counter(self):
      for counter, text in enumerate(self.texts):
         counter += 1
         if (counter % 100000) == 0:
            print(counter)
         if type(text) != type(None):
            for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
               elem = elem.split('\t')
               try:
                  #if not (self.isalnum_(elem[0])):
                  self.word_count[elem[0]] = self.word_count.get(elem[0], 0) + 1
                  self.total_words += 1
               except(IndexError):
                  continue

   # This method counts num of each noun in self.texts and store into self.noun_count
   # e.g. noun_count = { noun1:4, noun2:5, noun3:10, .....}
   def noun_counter(self):
      for counter, text in enumerate(self.texts):
         counter += 1
         if (counter % 100000) == 0:
            print(counter)
         if type(text) != type(None):
            for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
               elem = elem.split('\t')
               try:
                  if elem[3][0:2] == '名詞':
                     if not (self.isalnum_(elem[0])):
                        self.noun_count[elem[0]] = self.noun_count.get(elem[0], 0) + 1
                        self.total_noun += 1
               except(IndexError):
                  continue

   
   def adj_counter(self):
      for counter, text in enumerate(self.texts):
         counter += 1
         if (counter % 100000) == 0:
            print(counter)
         if type(text) != type(None):
            for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
               elem = elem.split('\t')
               try:
                  if elem[3][0:3] == '形容詞':
                     if not (self.isalnum_(elem[0])):
                        self.adj_count[elem[0]] = self.adj_count.get(elem[0], 0) + 1
                        self.total_adj += 1
               except(IndexError):
                  continue
   
   
   def verb_counter(self):
      for counter, text in enumerate(self.texts):
         counter += 1
         if (counter % 100000) == 0:
            print(counter)
         if type(text) != type(None):
            for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
               elem = elem.split('\t')
               try:
                  if elem[3][0:2] == '動詞':
                     if not (self.isalnum_(elem[0])):
                        self.verb_count[elem[0]] = self.verb_count.get(elem[0], 0) + 1
                        self.total_verb += 1
               except(IndexError):
                  continue

   def word_ranker(self, word, filename):
      with open(filename, 'w') as f:
         for k,v in sorted(word.items(), key=lambda x:x[1])[::-1]:
            f.write(k+'\t'+str(v) + '\n')

   def histgram(self, outfile):
      hist = [0]*24
      init_time = 4
      last_i = 0
      for i, date in enumerate(self.dates):
         if date:
            time = int(date.split(" ")[1][0:2])
            if time != init_time:
               hist[init_time] = i - last_i + 1
               last_i = i
               if init_time == 23:
                  init_time = 0
               else:
                  init_time += 1
      x_label = [ str(i) for i in range(24)]
      x_label = x_label[4:] + x_label[0:4]
      hist[init_time] = i - last_i + 1
      hist = hist[4:] + hist[0:4]
      plt.bar(x_label, hist)
      plt.title(outfile)
      plt.savefig('data/2_hist/'+outfile)

if __name__=='__main__':
   reader = TweetReader()
   reader.read_lines(sys.argv[1])
   reader.getContexts()
   reader.word_counter()
   print(reader.word_count)
   reader.word_ranker(reader.word_count, sys.argv[2])
