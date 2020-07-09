def str2bytes(s):
	return bytes(s,'utf-8')

def xor(b1, b2):
	ret = bytearray()
	for i,j in zip(b1,b2):
		ret.append(i^j)
	return bytes(ret)

def pad(ciphertext,size):
	if (type(ciphertext) != bytes):
		print("pad expects bytes")
		return

	ret = bytearray()
	for b in ciphertext:
		ret.append(b)
	
	remainder = size - (len(ciphertext) % size)

	for pad in range(remainder):
		ret.append(remainder)
	return bytes(ret)