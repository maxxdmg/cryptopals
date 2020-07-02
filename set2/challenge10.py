from Crypto.Cipher import AES
import base64
import sys
sys.path.insert(1, '../tools/')
import CBC as c

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


block_size = 16
key = "YELLOW SUBMARINE"
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
cryptsys = AES.new(key, AES.MODE_ECB)

with open("10.txt") as fh:
        ciphertext = base64.b64decode(fh.read())
'''
cipherblocks = [ciphertext[i:i+block_size] for i in range(0,len(ciphertext),block_size)]
print(cbc_decrypt(cipherblocks,iv,cryptsys))
'''
print(c.make_blocks(ciphertext, block_size))