import requests
import sys
import random
import json
import getopt
import os.path

#TODO support newlines, do something about omitted chars due to not being present in content source

def getRandomIndex(charIndex, ch):
	return charIndex[ch][random.randint(0, len( charIndex[ch])-1 ) ]

def encode_from_url(url, plaintext):
	content = requests.get(url).content.decode()
	return encode(content, plaintext)

def encode(content, plaintext):
	index = indexSiteChars(content)
	return genCipherText(plaintext, index)

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

def decode_from_url(url, ciphertext):
	content = requests.get(url).content.decode()
	return decode(content, ciphertext)

def decode(content, ciphertext):
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
	




BOOK = sys.argv[1]

#read input plain or ciphertext
f = open(infile, 'r')
fcontent = f.read()
f.close()

#determine if its a url or a file
if os.path.isfile(BOOK):
	bf = open(BOOK, 'r')
	content = bf.read()
	bf.close()
	if DECODE:
		print(decode(content, json.loads(fcontent)))
	else:
		print(encode(content, fcontent))
else:
	URL = BOOK	#just for clarity
	if DECODE:
		print(decode_from_url(URL, json.loads(fcontent)))
	else:
		print(encode_from_url(URL, fcontent))

sys.exit(0)


