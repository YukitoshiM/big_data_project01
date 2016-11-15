import sys
import reader
import MeCab

read = reader.TweetReader()
read.read_lines(sys.argv[2])
read.getIDs()
read.getContexts()
read.read_corpus()

tagger = MeCab.Tagger('-Ochasen')

def open_file(filename):
   ret_val = []
   with open(filename, 'r') as f:
      lines = f.readlines()
   for i, line in enumerate(lines):
      if i == 0:
         continue
      line = line.replace('\n','').split(' ')
      ret_val.append(line)
   return ret_val

def acount_by_class(results):
   class0, class1, class2 = [], [], []
   for res in results:
      if res[0] == '0':
         class0.append(res[-1])
      elif res[0] == '1':
         class1.append(res[-1])
      elif res[0] == '2':
         class2.append(res[-1])
      else:
         print('Warning: This Method does not take more than 3 classes, so ad if statement to cover more')
   return class0, class1, class2

def tweet_by_class(classes, n=2):
   list0, list1, list2 = [], [], []
   for ac, text in zip(read.ids, read.texts):
      if ac in classes[0]:
         list0.append(text)
      if ac in classes[1]:
         list1.append(text)
   if n == 3:
      for ac, text in zip(read.ids, read.texts):
         if ac in classes[2]:
            list0.append(text)
   return list0, list1, list2

def count_word(List):
   word_dict0, word_dict1, word_dict2 = {}, {}, {}
   for word in read.corpList:
      word_dict0.update({word[0]:0})
      word_dict1.update({word[0]:0})
      word_dict2.update({word[0]:0})
   for text in List[0]:
      if text:
         for word in mecab(text):
            word = getWord(word)
            if word in word_dict0:
               word_dict0[word] += 1
   for text in List[1]:
      if text:
         for word in mecab(text):
            word = getWord(word)
            if word in word_dict1:
               word_dict1[word] += 1
   for text in List[2]:
      if text:
         for word in mecab(text):
            word = getWord(word)
            if word in word_dict2:
               word_dict2[word] += 1
   return word_dict0, word_dict1, word_dict2
   
def mecab(text):
   return tagger.parse(text.replace(' ','').replace('EOS', '')).split('\n')
   
def getWord(tag):
   try:
      return tag.split('\t')[2]
   except:
      return None

def display(dicts):
   print('Class 0:')
   for k, v in sorted(dicts[0].items(), key=lambda x:x[1], reverse=True):
      if v != 0:
         print(k, v)
   print('\nClass 1:')
   for k, v in sorted(dicts[1].items(), key=lambda x:x[1], reverse=True):
      if v != 0:
         print(k, v)
   print('\nClass 2:')
   for k, v in sorted(dicts[2].items(), key=lambda x:x[1], reverse=True):
      if v != 0:
         print(k, v)



def main():
   results = open_file(sys.argv[1])
   class0, class1, class2 = acount_by_class(results)
   list0, list1, list2 = tweet_by_class( (class0,class1,class2))
   dict0, dict1, dict2 = count_word((list0, list1, list2))
   display((dict0, dict1, dict2))

if __name__=='__main__':
   main()
