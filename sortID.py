import sys
import reader
import MeCab

def sort_file(inFile, outFile):
   read = reader.TweetReader()
   tagger = MeCab.Tagger('-Ochasen')
   read.read_lines(inFile)
   read.getIDs()
   read.getDates()
   read.getContexts()
   newTextList = []
   for i, text in enumerate(read.texts):
      if read.dates[i] and text:
         new_text = read.dates[i] + '\t'
         for tag in tagger.parse(text.replace(' ','')).split('\n'):
            try:
               tag = tag.split('\t')
               pos = tag[3].split('-')[0]
               if not (pos == '助詞' or pos == '助動詞' or pos == '記号'):
                  new_text += tag[2] + '-' + pos + '\t'
            except:
               # Ignore EOS
               continue
         newTextList.append(new_text + '\n')
   with open(outFile, 'w') as f:
      for l in newTextList:
         f.write(l)

if __name__=='__main__':
   sort_file(sys.argv[1], sys.argv[2])
