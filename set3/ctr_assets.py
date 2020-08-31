from Crypto.Cipher import AES
from random import randrange
import base64
import struct

def blockify(string, size):
	ret = []
	for i in range( 0, len(string), size ):
		ret.append( string[ i : i + size ] )
	return ret

def concat_bytes(first,last):
	ret = bytearray()
	for byte in first:
		ret.append(byte)
	for byte in last:
		ret.append(byte)
	return ret

def xor(block0, block1):
	ret = bytearray()
	for (a,b) in zip(block0,block1):
		ret.append(a^b)
	return bytes(ret)

def copy_bytes(a):
	ret = bytearray()
	for b in a:
		ret.append(b)
	return ret

def generate_key():
	ret = bytearray()
	for i in range(16):
		ret.append( randrange(64,128) )
	return bytes(ret)

def ctr_single_block_encrypt( block, cipher, nonce, counter ):
	keystream = cipher.encrypt( struct.pack('<QQ', nonce, counter) )
	return xor( block, keystream )

def ctr_encrypt( blocks, cipher, nonce ):
	cipherblocks = []
	counter = 0

	for block in blocks:
		cipherblocks.append( ctr_single_block_encrypt( block, cipher, nonce, counter ) )
		counter += 1
	return cipherblocks

def ctr_decrypt( cipherblocks, cipher, nonce ):
	return ctr_encrypt( cipherblocks, cipher, nonce )