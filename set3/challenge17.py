from Crypto.Cipher import AES
from cbc_assets import cbc_encrypt, cbc_decrypt, pad_pcks7, validate_pcks7, collapse_byteblocks, copy_bytes, concat_bytes
from random import randint

def encrypt():
	size = 16
	iv = b'0' * size
	key = b'bY|d[]CJgLhCxuuj' #generate_key() generated one time
	ciphersys = ciphersys = AES.new(key, AES.MODE_ECB)

	# select one of these strings
	strings = [
		b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
		b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
		b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
		b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
		b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
		b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
		b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
		b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
		b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
		b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
	]
	string = strings[ randint( 0, len(strings)-1 ) ]

	# return cbc ciphertext and iv
	return ( cbc_encrypt( string, iv, ciphersys, size ), iv )


def validate( blocks, size ):
	try:
		validate_pcks7( collapse_byteblocks( blocks ), size )
		return True
	except:
		return False

def decrypt( cipherblocks, iv ):
	size = 16
	key = b'bY|d[]CJgLhCxuuj' #generate_key() generated one time
	ciphersys = ciphersys = AES.new(key, AES.MODE_ECB)
	return validate( cbc_decrypt( cipherblocks, iv, ciphersys ), size )

def attack_byte( blocks, targetblock, targetbyte ):
	ret = 0
	for j in range(256): 
		blocks[0][targetbyte] = j
		x = decrypt( [ bytes( block ) for block in blocks ], iv )
		if x == True:
			ret = j
			return ret
	
	return ret

def recalc_corruptedblock(cipherblock, plainbytes, pad, size):
	ret = bytearray()
	for i in range( size ):
		ret.append( 0 )

	loops = 0
	while loops < pad-1:
		newbyte = pad ^ cipherblock[ -1 - ( loops ) ] ^ plainbytes[ -1 - ( loops ) ]
		ret[ -1 - ( loops ) ] = newbyte
		loops += 1
	return ret

def replace_bytes( dest, src ):
	new_dest = copy_bytes( dest )
	for b in range(len(src)):
		new_dest[b] = src[b]
	dest = new_dest



e = encrypt()
cipherblocks = e[0]

iv = e[1]
size = 16
known_blocks = []
for a in range( len(cipherblocks) ):
	plainbytes = []
	pad = 1
	targetblock = len(cipherblocks) - 2 - a
	targetbyte = len(cipherblocks[ targetblock ]) - 1
	# set our malicious controlled block to all zeros

	corruptedblocks = [ copy_bytes( cipherblocks[i] ) for i in range( len(cipherblocks)-2-a, len(cipherblocks)-a, 1) ]
	for i in range( len(corruptedblocks[0]) ):
		corruptedblocks[0][i] = 0

	curr_cipherbyte = iv[targetbyte]
	if targetblock > -1:
		curr_cipherbyte = cipherblocks[targetblock][targetbyte]
	curr_corruptedbyte = attack_byte( corruptedblocks, 0, targetbyte )

	# crack the last new byte of plaintext
	plainbyte = curr_corruptedbyte ^ pad ^ curr_cipherbyte
	plainbytes = [ plainbyte ] + plainbytes # prepend this plainbyte to the list of them
	# recalculate c` for a new padding length
	for k in range(15):
		pad += 1

		cipherblock = iv
		if targetblock > -1:
			cipherblock = cipherblocks[ targetblock ]
		corruptedblocks[ 0 ] = recalc_corruptedblock( cipherblock, plainbytes, pad, size )
		targetbyte -= 1

		curr_cipherbyte = iv[targetbyte]
		if targetblock > -1:
			curr_cipherbyte = cipherblocks[targetblock][targetbyte]

		curr_corruptedbyte = attack_byte( corruptedblocks, 0, targetbyte )
		# crack a new byte of plaintext
		plainbyte = curr_corruptedbyte ^ pad ^ curr_cipherbyte
		plainbytes = [ plainbyte ] + plainbytes # prepend this plainbyte to the list of them
	known_blocks = [ bytes(plainbytes) ] + known_blocks

plaintext = ''
for block in known_blocks:
	plaintext +=  ''.join( [ chr(b) for b in block ] )
print("Decrypted string: ", plaintext)