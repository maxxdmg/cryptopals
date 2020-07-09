from Crypto.Cipher import AES
from PKCS7_padding import pad, str2bytes, xor

def build_system(key, blocksize):
	return AES.new(pad(key, blocksize), AES.MODE_ECB)

def make_blocks(text, blocksize):
	l = len(text)
	ret = [text[i:i+blocksize] for i in range(0, l, blocksize)]
	if (l-1) % blocksize > 0:
		ret.append(pad(text[l-1-blocksize:], blocksize))
	return ret		

def encrypt(plainblocks, iv, sys):
	cipherblocks = [sys.encrypt(xor(plainblocks[0], iv))]
	for i in range(1, len(plainblocks), 1):
		xorblock = xor(plainblocks[i], cipherblocks[i-1])
		cipherblocks.append(sys.encrypt(xorblock))
	return cipherblocks

def decrypt(cipherblocks, iv, sys):
	plainblocks = []
	for i in range(len(cipherblocks-1), 1, -1):
		dblock = sys.decrypt(cipherblock[i])
		plainblocks.append(xor(dblock, cipherblock[i-1]))
	dblock = sys.decrypt(cipherblock[0])
	plainblocks.append(xor(dblock, iv))
	return plainblocks

'''
TESTS
blocksize = 16
ciphersys = build_system(str2bytes("test"), blocksize)

iv = bytearray()
for i in range(16):
	iv.append(1)
iv = bytes(iv)

ciphertext = encrypt(str2bytes("data"), iv, blocksize, ciphersys)
print(ciphertext)

pt = decrypt(ciphertext, iv, blocksize, ciphersys)
print(pt)
'''

