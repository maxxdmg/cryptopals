import binascii

def single_byte_xor (x):
	# decode hex
	hex_str = binascii.unhexlify(x)
	# attempt byte combinations
	for key in range(256):
		# xor each previously decoded hex byte w/ attempted key byte
		result = ''.join(chr(bit ^ key) for bit in hex_str)
		# possible solution if result is all ascii printable & contains a space
		if result.isprintable() and result.find(' ') != -1:
			print("key: " + str(key))
			print(result)
single_byte_xor("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
