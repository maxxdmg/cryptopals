def xor(x, y):
	# get int values for x & y
	x = format(ord(x), 'x')
	y = format(ord(y), 'x')
	xor = int(x, 16) ^ int(y, 16) # xor the hex ints
	result = format(xor, 'x')
	# check if length 1 value then format w/ extra 0
	if (len(result) < 2):
		return result.zfill(2)
	return result # otherwise return the result

def encrypt (plaintext, key):
	counter = 0
	ciphertext = ""
	# loop through all chars of plaintext
	for char in plaintext:
		key_char = key[counter % len(key)] # get current key char
		counter += 1 # increment counter
		ciphertext += xor(char, key_char) # get xor'd characters and add to ciphertext
	print(ciphertext)
	return ciphertext

plaintext = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
key = "ICE"
encrypt(plaintext, key)