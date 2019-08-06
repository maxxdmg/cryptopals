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
	for letter in x:
		if letter in scores:
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
	print(result)
	return result
single_byte_xor("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")