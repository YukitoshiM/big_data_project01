# This program reads crowled Tweeter data

import sys

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

if __name__=='__main__':
   reader = TweetReader()
   reader.create_lists(sys.argv[1])
