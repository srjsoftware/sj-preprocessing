#
#	Copyright (C) 2017 by Sidney Ribeiro Junior
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


import hashlib
import sys
import operator
import time
import re

def clean(s):
	return re.sub(r'[-!@#$%^&*()_+=\[\]{}\|`~;:\'"<>?,./]', '', re.sub(' +', ' ', re.sub(r'\t', ' ', s))).lower()

def getQgram(line, i, count, q):
	if q == 2:
		return line[i] + line[i+1] + str(count)
	elif q == 3:
		return line[i] + line[i+1] + line[i+2] + str(count)


if len(sys.argv) < 3:
	print "Too few arguments"
	exit()
	
arquivo = open(sys.argv[1], "r")
lines = arquivo.readlines()
q = int(sys.argv[2])
sets = []


qgramsets = []
dictionary = {}

start = time.time()

# Convert to q-gram and build dictionary:

for line in lines:
	i = 0
	setx = []
	line = (q-1)*'_' + clean(line).rstrip() + (q-1)*'_'
	for char in line:
		if i + q - 1 < len(line):
			count = 0;
			qgram = getQgram(line, i, count, q)
			while setx.count(qgram) == 1:
				count = count + 1
				qgram = getQgram(line, i, count, q)
			setx.append(qgram)
			
			if qgram in dictionary:
				dictionary[qgram] = dictionary[qgram] + 1
			else:
				dictionary[qgram] = 1
		i += 1
	qgramsets.append(setx)

end = time.time()
#print("time to tokenize and build dictionary: " + str((end - start)))

#sort by inverted frequency
start = time.time()

dictOrdered = sorted(dictionary.items(), key=operator.itemgetter(1))

end = time.time()
#print("sorting dictionary time: " + str((end - start)))

i = 0
ids = {}

start = time.time()

# creates ids for dictionary q-grams (0 = least frequent, 1 = second least frequente...)
for key, val in dictOrdered:
	ids[key] = i
	i += 1

end = time.time()
#print("time to set ids on dictionary: " + str((end - start)))

allsets = []

start = time.time()

# changes q-grams for ids and sort by frequency
for setx in qgramsets:
	newset = []
	for qgram in setx:
		newset.append(ids[qgram])
	allsets.append(sorted(newset))

end = time.time()
#print("time to substitute qgrams for ids and sorting sets: " + str((end - start)))


start = time.time()

# sorts set by size
orderedBySize = sorted(allsets, key=len)

end = time.time()
#print("time to sort collection by set size: " + str((end - start)))

# sf-gSSJoin format:

output = open(sys.argv[1] + '_q' + str(q), 'w')

for setx in orderedBySize:
	for qgram in setx:
		output.write(str(qgram) + " ")
	output.write("\n")
	
exit()
