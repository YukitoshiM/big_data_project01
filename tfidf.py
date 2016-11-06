def getTF(self, word, text):
    numOfWords = 0
    for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
       elem = elem.split('\t')
       if elem[0] == word:
          numOfWords += 1
    return numOfWords / total_words

def getDF(self, word):
   numOfText = 0
   word_flag = False
   for counter, text in enumerate(self.texts):
      counter += 1
      if (counter % 100000) == 0:
         print(counter)
      if type(text) != type(None):
         for elem in self.tagger.parse(text.replace(' ','')).split('\n'):
            elem = elem.split('\t')
            if elem[0] == word:
               word_flag = True
      if word_flag:
         numOfText += 1
      word_flag = False
      return numOfText

def getIDF(self, word):
   df = self.getDF(word)
   n = len(self.contexts)
   return math.log2(n/df)

166    def getTFIDF(self, word, text):
167       tf = self.getTF(word, text)
168       idf = self.getIDF(word)
169       return tf*idf
