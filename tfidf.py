#coding:utf-8
import sys
import math
from collections import OrderedDict
def time_check(t):
	t = t - int(base)
	if t < 0:
		t += 60 
	if t < time :
		return 0
	else :
		return 1
argvs = sys.argv
file = open(argvs[1])
time = 30
base = 0
first_line = 1
ID_dic = OrderedDict()
time_dic = OrderedDict()
number_count = 0
df = {}
tf = {}
for line in file:
	seps = line.split("\t")
	times = seps[0].split(":")
	if first_line == 1 :
		first_line = 0
		label = seps[0]
		base = int(times[1])
	if time_check(int(times[1])):
		for key in tf.keys():
			if key not in df:
				df[key] = 1
			else:
				df[key] += 1
		time_dic[label] = tf
		label = seps[0]
		base = int(times[1])
		tf = {}
		
	for wordfeat in seps[1:-1]:
		word = wordfeat.split("-")
		if word[0] not in ID_dic:
			ID_dic[word[0]] = number_count
			number_count += 1
		if ID_dic[word[0]] not in tf:
			tf[ID_dic[word[0]]] = 1
		else:
			tf[ID_dic[word[0]]] += 1
out_s = "features\t"
for k,v in ID_dic.items():
	out_s += k + "\t"
print(out_s[:-1])

for k,v in time_dic.items():
	out_s = k + "\t"
	rem_n = 0
	for word,tf in v.items():
		while(rem_n<word):
			rem_n +=1
			out_s += "0\t"			
		out_s += str(tf*math.log10(df[word])+1) + "\t"
		rem_n += 1
	while(rem_n<=len(df)):
		out_s += "0\t"
		rem_n += 1
	print(out_s[:-1])
#for k,v in sorted(dic.items()):
#	for sep in v:
#		print(sep)

