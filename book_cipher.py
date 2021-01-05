import requests
import sys
import random
import json
import getopt

def getRandomIndex(charIndex, ch):
	return charIndex[ch][random.randint(0, len( charIndex[ch])-1 ) ]

def genCipherText(msg, charIndex):
	ciphertext = []
	for ch in msg:
		if ch in charIndex:
			ciphertext.append(getRandomIndex(charIndex, ch))
	return ciphertext


def indexSiteChars(content): 
	index = {}
	lineIndex = 0
	charIndex = 0

	lines = content.split("\n")

	for line in lines:
		for ch in line:
			if ch not in index:
				index[ch] = [ [lineIndex, charIndex] ]
			else:
				index[ch].append([lineIndex, charIndex])
			charIndex = charIndex + 1
		lineIndex = lineIndex + 1
		charIndex = 0
	return index

def decode(url, ciphertext):
	content = requests.get(url).content.decode()
	lines = content.split("\n")
	plaintext = ""
	for coord in ciphertext:
		plaintext = plaintext + lines[coord[0]][coord[1]]
	return plaintext


try:
	opts, args = getopt.getopt(sys.argv[2:], 'd:e:')
except getopt.GetoptError:
	print("Usage: URL [-d|-e] inputfile")
	sys.exit(2)

DECODE = False
infile = None
for opt, arg in opts:
	if opt == '-d':
		infile = arg
		DECODE = True
		break
	if opt == '-e':
		infile = arg
		break
	




URL = sys.argv[1]
f = open(infile, 'r')
fcontent = f.read()
f.close()

if DECODE:
	print(decode(URL, json.loads(fcontent)))
else:
	r = requests.get(URL)
	index = indexSiteChars(r.content.decode())
	ciphertext = genCipherText(fcontent, index)
	print(ciphertext)

sys.exit(0)


