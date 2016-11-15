import sys

def open_file(filename):
   ret_val = []
   with open(filename, 'r') as f:
      lines = f.readlines()
   for i, line in enumerate(lines):
      if i == 0:
         continue
      line = line.replace('\n','').split(' ')
      ret_val.append(line)
      print(line[4])
   return ret_val

def acount_by_class(results):
   class0, class1, class2 = [], [], []
   for res in results:
      print(res)
      if res[0] == '0':
         class0.append(res[3])
      elif res[0] == '1':
         class1.append(res[3])
      elif res[0] == '2':
         class2.append(res[3])
      else:
         print('Warning: This Method does not take more than 3 classes, so ad if statement to cover more')
   return class0, class1, class2

def main():
   results = open_file(sys.argv[1])
   class0, class1, class2 = acount_by_class(results)
   print(class0)

if __name__=='__main__':
   main()
