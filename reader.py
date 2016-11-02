# This program reads crowled Tweeter data

import sys
import MeCab as Mecab
from collections import defaultdict

# class for reading Tweeter data for any given file 
class TweetReader():
   def __init__(self):
      # These list prepared for data in the Tweeter, 
      # First 4 variables prepared for a line which is devided by tab space
      # Last 3 are for contexts that is devided by space
      # rt_flags: contains if the tweet is retweet or not
      # reps:     contains for whom the tweet was replied 
      # texts:    contains actual tweet message
      self.ids, self.dates, self.contexts, self.unk_nums, self.rt_flags, self.reps, self.texts, self.lines, self.morpho= [], [], [], [], [], [], [], [], []
      self.noun_count, self.adj_count = defaultdict(int), {}

   # This method read lines in the input file and store it into class variable called self.lines
   def read_lines(self, filename):
      with open(filename, 'r') as f:
         self.lines = f.readlines()
      for i, line in enumerate(self.lines):
         if line == '\n':
            self.lines.pop(i)

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
               self.texts.append(''.join(context[2:]))
            except:
               self.rt_flags.append(0)
               self.reps.append(None)
               self.texts.append(None)
               continue
         elif context[0] == '@':
            context = context.split()
            self.rt_flags.append(0)
            self.reps.append(context[0])
            self.texts.append(''.join(context[1:]))
         else:
            self.rt_flags.append(0)
            self.reps.append(None)
            self.texts.append(context)

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
  
   def noun_counter(self):
      tagger = Mecab.Tagger('-Ochasen')
      for counter, text in enumerate(self.texts):
         counter += 1
         if (counter % 100000) == 0:
            print(counter)
         if type(text) != type(None):
            for elem in tagger.parse(text.replace(' ','')).split('\n'):
               elem = elem.split('\t')
               try:
                  if elem[3][0:2] == '名詞':
                     self.noun_count[elem[0]] = self.noun_count.get(elem[0], 0) + 1
               except(IndexError):
                  continue


"""   def create_lists(self, filename):
      # reads files and save lines in to a list
      with open(filename, 'r') as f:
         lines = f.readlines()

      # This line assignes empty lists if the method is called more than twice
      self.ids, self.dates, self.contexts, self.unk_nums, self.rt_flags, self.reps, self.texts = [], [], [], [], [], [], []

      # for each line of file
      for line in lines:
         # this if statement ignore only if the lien is new line(sometime, this happen)
         if line == '\n':
            continue
         # Firstable, devide line by tab sapace, and maximum list size is 4
         # For some line, lists' size is less than 4
         # 1st case: contains only message(context)
         # 2nd case: contains messages and unknown numbers
         # 3rd case: missing unknown numbers
         temp_split = line.split('\t')
         if len(temp_split) == 1:
            self.ids.append( None )
            self.dates.append( None )
            self.contexts.append( temp_split[0] )
            self.unk_nums.append( None )
         elif len(temp_split) == 2:
            self.ids.append( None )
            self.dates.append( None )
            self.contexts.append( temp_split[0] )
            self.unk_nums.append( temp_split[1] )
         elif len(temp_split) == 3:
            self.ids.append( temp_split[0] )
            self.dates.append( temp_split[1] )
            self.contexts.append( temp_split[2] )
            self.unk_nums.append( None )
         elif len(temp_split) == 4:
            self.ids.append( temp_split[0] )
            self.dates.append( temp_split[1] )
            self.contexts.append( temp_split[2])
            self.unk_nums.append( temp_split[3] )
      
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
               self.texts.append(' '.join(context[2:]))
            except:
               self.rt_flags.append(0)
               self.reps.append(None)
               self.texts.append(None)
               continue
         elif context[0] == '@':
            context = context.split()
            self.rt_flags.append(0)
            self.reps.append(context[0])
            self.texts.append(' '.join(context[1:]))
         else:
            self.rt_flags.append(0)
            self.reps.append(None)
            self.texts.append(context)"""

if __name__=='__main__':
   reader = TweetReader()
   reader.read_lines(sys.argv[1])
   reader.getContexts()
   reader.noun_counter()
