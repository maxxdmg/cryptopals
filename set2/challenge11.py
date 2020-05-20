from Crypto.Cipher import AES
from random import randrange
import base64

def xor(block0, block1):
	ret = bytearray()
	for (a,b) in zip(block0,block1):
		ret.append(a^b)
	return bytes(ret)


def cbc_encrypt(plainblocks, iv, cipher):
	ret = []
	prev_block = iv
	
	for p in plainblocks:
		prev_block = cipher.encrypt( xor(p, prev_block) )
		ret.append(prev_block)
	
	return ret

def cbc_decrypt(cipherblocks, iv, cipher):
	ret = []
	prev_block = iv

	for c in cipherblocks:
		print(c)
		ret.append(xor(cipher.decrypt(c), prev_block))
		prev_block = c
	return ret

def generate_key():
	ret = bytearray()
	for i in range(16):
		ret.append( randrange(64,128) )
	return bytes(ret)

def unknown_encrypt(plaintext):
	key = generate_key()
	block_size = 16
	iv = generate_key() # should work for rand iv generation
	cryptsys = AES.new(key, AES.MODE_ECB)

	prepad = "".join( [chr(randrange(64,128)) for i in range(0,randrange(6,10),1) ] )
	postpad = "".join( [chr(randrange(64,128)) for i in range(0,16-len(prepad),1) ] )

	ciphertext = cryptsys.encrypt(prepad + plaintext + postpad)
	
	return [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

'''
block_size = 16
key = "YELLOW SUBMARINE"
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
cryptsys = AES.new(key, AES.MODE_ECB)

with open("10.txt") as fh:
        ciphertext = base64.b64decode(fh.read())
cipherblocks = [ciphertext[i:i+block_size] for i in range(0,len(ciphertext),block_size)]
print(cbc_decrypt(cipherblocks,iv,cryptsys))
'''
correct = 0
for count in range(100):
	plaintext = "".join(["A" for i in range(0,32,1)])
	cipherblocks = unknown_encrypt(plaintext)

	ecb = False
	for cipher in cipherblocks:
		if ( len(cipher) - len(set(cipher)) != 0):
			ecb = True
			break

	if (ecb):
		correct += 1

print(str((correct / 100) * 100) + "% accuracy")


