import sys

def validate_pcks7(text, blocksize):
	pad = int.from_bytes(text[-1:], sys.byteorder)
	n = text.count(text[-1:], -pad)
	if n != pad:
	    raise ValueError
	return text[:-pad]

def test():
	test1 = b'ICE ICE BABY\x04\x04\x04\x04'
	test2 = b'ICE ICE BABY\x05\x05\x05\x05'
	test3 = b'ICE ICE BABY\x01\x02\x03\x04'
	
	# test 1
	res = validate_pcks7(test1, 16)
	if res == b'ICE ICE BABY':
		print("PASS")
	else:
		print("FAIL")
		exit(1)

	# test 2
	try:
		res = validate_pcks7(test2, 16)

		print("FAIL")
		exit(1)
	except ValueError:
		print("PASS")

	#test 3
	try:
		res = validate_pcks7(test3, 16)

		print("FAIL")
		exit(1)
	except ValueError:
		print("PASS")


#test()