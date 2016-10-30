# This program reads crowled Tweeter data

import sys
import MeCab as Mecab

# class for reading Tweeter data for any given file 
class TweetReader():
   def __init__(self):
      # These list prepared for data in the Tweeter, 
      # First 4 variables prepared for a line which is devided by tab space
      # Last 3 are for contexts that is devided by space
      # rt_flags: contains if the tweet is retweet or not
      # reps:     contains for whom the tweet was replied 
      # texts:    contains actual tweet message
      self.ids, self.dates, self.contexts, self.unk_nums, self.rt_flags, self.reps, self.texts = [], [], [], [], [], [], []
      self.noun_count, self.adj_count = {}, {}

   def create_lists(self, filename):
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
            self.texts.append(context)

   def word_counter(self):
      tagger = Mecab.Tagger('-Ochasen')
      # parse texts lines and split them by new line [str, str, str, ......]
      tagged_list = [ tagger.parse(text.replace(' ','')).split('\n') for text in self.texts if type(text) != type(None)]
      # split each text by tab
      tagged_list = [elem for elem in [outer.pop(0) if x == 'EOS' or x == '' else x.split('\t') for outer in tagged_list for x in outer]]
      # This method consume too much memory up to here!!!!!!!!
      noun_list, adj_list = [], []
      for elem in tagged_list:
         try:
            if elem[3][0:2] == '名詞':
               self.noun_count[elem[0]] = self.noun_count.get(elem[0], 0) + 1
            counter += 1
            """elif elem[3][0:3] == '形容':
               adj_list = elem[0]
               self.adj_count[elem[0]] = self.adj_count.get(elem[0], 0) + 1"""
         except(IndexError):
            continue
      print(self.noun_count)

if __name__=='__main__':
   reader = TweetReader()
   reader.create_lists(sys.argv[1])
   print('hello')
   reader.word_counter()
