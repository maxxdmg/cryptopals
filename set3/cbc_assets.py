from Crypto.Cipher import AES
from random import randrange
import base64
import sys

def validate_pcks7(text, blocksize):
	i = text[-1]
	if i == 0 or text[-i:] != bytes([i] * i):
		raise ValueError('bad padding')
	return text[0:-i]

def blockify(string, size):
	ret = []
	for i in range( 0, len(string), size ):
		ret.append( string[ i : i + size ] )
	return ret

def collapse_byteblocks( blocks ):
	ret = bytearray()
	for block in blocks:
		ret = concat_bytes( ret, block )		

	return bytes( ret )

def concat_bytes(first,last):
	ret = bytearray()
	for byte in first:
		ret.append(byte)
	for byte in last:
		ret.append(byte)
	return ret

def copy_bytes(a):
	ret = bytearray()
	for b in a:
		ret.append(b)
	return ret

def xor(block0, block1):
	ret = bytearray()
	for (a,b) in zip(block0,block1):
		ret.append(a^b)
	return bytes(ret)

def pad_pcks7(ciphertext,size):
	ret = bytearray()
	for b in ciphertext:
		ret.append(b)
	
	remainder = size - (len(ciphertext) % size)

	for pad in range(remainder):
		ret.append(remainder)
	return bytes(ret)

def rand_bytes(min_chars, max_chars):
	ret = bytearray()
	for i in range(randrange(min_chars,max_chars)):
		ret.append(randrange(64,128))
	return ret

def cbc_encrypt(plaintext, iv, cipher, size):
	plaintext = pad_pcks7( plaintext, size )
	blocks = blockify( plaintext, size )

	ret = []
	prev_block = iv
	for b in blocks:
		prev_block = cipher.encrypt( xor(b, prev_block) )
		ret.append(prev_block)
	
	return ret

def cbc_decrypt(cipherblocks, iv, cipher):
	ret = []
	prev_block = iv

	for c in cipherblocks:
		ret.append(xor(cipher.decrypt(c), prev_block))
		prev_block = c
	return ret

def generate_key():
	ret = bytearray()
	for i in range(16):
		ret.append( randrange(64,128) )
	return bytes(ret)