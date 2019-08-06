import binascii

def single_byte_xor (x):
	# decode hex
	hex_str = binascii.unhexlify(x)
	# attempt byte combinations
	for key in range(256):
		# xor each previously decoded hex byte w/ attempted key byte
		result = ''.join(chr(bit ^ key) for bit in hex_str)
		# possible solution if result is all ascii printable
		if result.isprintable():
			print("key: " + str(key))
			print("potential result: " + result)
	return result

def string_score (x):
	score = 0
	# calculate a score based on the most frequent english letters
	for char in x:
		if char == ' ':
			score += 13
			continue
		elif char == 'e':
			score += 12
			continue
		elif char == 't':
			score += 11
			continue
		elif char == 'a':
			score += 10
			continue
		elif char == 'o':
			score += 9
			continue
		elif char == 'i':
			score += 8
			continue
		elif char == 'n':
			score += 7
			continue
		elif char == 's':
			score += 6
			continue
		elif char == 'h':
			score += 5
			continue
		elif char == 'r':
			score += 4
			continue
		elif char == 'd':
			score += 3
			continue
		elif char == 'l':
			score += 2
			continue
		elif char == 'u':
			score += 1
			continue
	return score

import binascii

def score_plaintext (x):
	# map of letter frequency scores based on wikipedia chart
	scores = {
	  ' ':15,
	  'e':12.702,
	  't':9.056,
	  'a':8.167,
	  'o':7.507,
	  'i':6.966,
	  'n':6.749,
	  's':6.327,
	  'h':6.094,
	  'r':5.987,
	  'd':4.253,
	  'l':4.025,
	  'c':2.782,
	  'u':2.758,
	  'm':2.406,
	  'w':2.360,
	  'f':2.228,
	  'g':2.015,
	  'y':1.974,
	  'p':1.929,
	  'b':1.492,
	  'v':0.978,
	  'k':0.772,
	  'j':0.153,
	  'x':0.150,
	  'q':0.095,
	  'z':0.074
	}
	score = 0
	# score each letter in text to calculate overall score
	for letter in x.lower():
		if letter.lower() in scores:
			score += scores[letter]
		else:
			score -= 1
	return score

def single_byte_xor (x):
	hex_str = binascii.unhexlify(x) # decode hex
	candidates = []
	result = ""
	max_score = 0
	# attempt byte combinations
	for key in range(0,256):
		# xor each previously decoded hex byte w/ attempted key byte
		new_candidate = ''.join(chr(bit ^ key) for bit in hex_str)
		candidates.append(new_candidate) # add to candidates
	# loop thru candidates and find highest text score
	for candidate in candidates:
		new_score = score_plaintext(candidate)
		# deduce if new scored candidate is greater than current result
		if (new_score > max_score):
			max_score = new_score
			result = candidate
	return [result, max_score]

def detect_xor():
	f = open("./challenge4data.txt") # open data file as f
	scores = []
	results = []
	max_score = 0
	result = ""
	# loop through each line in file f
	for line in f:
		line = line.strip() # remove whitespace from line
		data = single_byte_xor(line) # calculate score & result for the line
		results.append(data[0])
		scores.append(data[1])
	# loop through all found results & scores
	for i in range(0,len(results)):
		# check if a higher scored result has been hit
		if scores[i] > max_score:
			max_score = scores[i]
			result = results[i]
	print(result)
	return result

detect_xor()