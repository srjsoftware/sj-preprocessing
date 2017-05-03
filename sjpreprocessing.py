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

# Converte pra q-gram e monta o dicionario:



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


# Ordena inversamente por frequencia
start = time.time()

dictOrdered = sorted(dictionary.items(), key=operator.itemgetter(1))

end = time.time()
#print("sorting dictionary time: " + str((end - start)))

i = 0
ids = {}

start = time.time()

# cria ids para os itens do dicionario de qgrams (0 = menos frequente, 1 = segundo menos frequente...)
for key, val in dictOrdered:
	ids[key] = i
	i += 1

end = time.time()
#print("time to set ids on dictionary: " + str((end - start)))

allsets = []

start = time.time()

# substitui qgrams por ids e ordena internamente pela frequencia
for setx in qgramsets:
	newset = []
	for qgram in setx:
		newset.append(ids[qgram])
	allsets.append(sorted(newset))

end = time.time()
#print("time to substitute qgrams for ids and sorting sets: " + str((end - start)))


start = time.time()

# ordena conjuntos pelo tamanho
orderedBySize = sorted(allsets, key=len)

end = time.time()
#print("time to sort collection by set size: " + str((end - start)))

# imprimir
for setx in orderedBySize:
	for qgram in setx:
		sys.stdout.write(str(qgram) + " ")
	print ""
	
exit()


#gSSJoin format:

i = 0

for setx in orderedBySize:
	sys.stdout.write(str(i) + " 0 ")
	i += 1
	for qgram in setx:
		sys.stdout.write(str(qgram) + " 1 ")
	print ""
