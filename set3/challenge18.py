from Crypto.Cipher import AES
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

def ctr_encrypt( blocks, cipher, nonce ):
	cipherblocks = []
	counter = 0

	for block in blocks:
		keystream = cipher.encrypt( struct.pack('<QQ', nonce, counter) )
		
		print( keystream )

		counter += 1
		cipherblocks.append( xor( block, keystream ) )

	return cipherblocks

def ctr_decrypt( cipherblocks, cipher, nonce ):
	return ctr_encrypt( cipherblocks, cipher, nonce )

key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)
block_size = 16
nonce = 0

ct = blockify( base64.b64decode( b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==' ), block_size )
print( b''.join( ctr_decrypt( ct, cipher, nonce ) )  )
