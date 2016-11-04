import sys

def sort_file(inFile, outFile):
   dic = {}
   with open(inFile, 'r') as f:
      lines = f.readlines()
   lines = open(inFile)
   for line in lines:
      seps = line.split('\t')
      try:
         key = seps[1].replace("\r\n","").replace("-", "").replace(":", "").replace(" ", "").replace("+0000", "")
      except(IndexError):
         continue
      if key in dic:
         dic[key].append(line)
      else:
         dic[key] = [line]
   with open(outFile, 'w') as f:
      for k,v in sorted(dic.items()):
         for sep in v:
            f.write(sep)

if __name__=='__main__':
   sort_file(sys.argv[1], sys.argv[2])
