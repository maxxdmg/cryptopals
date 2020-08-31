from Crypto.Cipher import AES
from ctr_assets import ctr_encrypt, ctr_decrypt, concat_bytes, generate_key, blockify, xor
from base64 import b64decode
import struct
import string


'''
Break fixed-nonce CTR mode using substitutions
'''

def get_english_score(input_bytes):
    freq = {
    	'a': 1, 'b': 1, 'c': 1, 'd': 1,
        'e': 1, 'f': 1, 'g': 1, 'h': 1,
        'i': 1, 'j': 1, 'k': 1, 'l': 1,
        'm': 1, 'n': 1, 'o': 1, 'p': 1,
        'q': 1, 'r': 1, 's': 1, 't': 1,
        'u': 1, 'v': 1, 'w': 1, 'x': 1,
        'y': 1, 'z': 1, ' ': 1
    }

    return sum([freq.get(chr(byte), 0) for byte in input_bytes.lower()])


def single_char_xor(input_bytes, char_value):
    ret = b''

    for byte in input_bytes:
        ret += bytes([byte ^ char_value])
    
    return ret


def crack_nth_byte( nth_bytes ):
	max_score = -1
	pbyte = -1

	for keybyte in range( 256 ):
		score = get_english_score( single_char_xor( nth_bytes, keybyte ) )

		if score > max_score:
			max_score = score
			pbyte = keybyte

	return pbyte


def crack( ciphertexts ):
	key = []

	for target_index in range(max(map(len, ciphertexts))):
		target_bytes = []

		for c in ciphertexts:

			target_bytes.append( c[target_index] ) if target_index < len(c) else b''

		new_key_byte = crack_nth_byte( target_bytes )

		key.append( new_key_byte )

	for c in ciphertexts:
		p = b''
		for ch, k in zip(c,key):
			p += bytes( [ch ^ k] )
		print( p )



def encryptor( cipher ):
	# set up cipher and necessary values
	block_size = 16
	nonce = 0 # this is what causes the vulnerability

	# parse the base64 encoded plaintexts from provided file
	plaintexts = []
	ciphertexts = []
	f = open( "challenge19.txt" )

	for line in f:
		 plaintexts.append( b64decode( line.strip( '\n' ) ) )

	# turn the plaintexts into blocks and encrypt them
	for pt in plaintexts:
		new_cipherblocks = ctr_encrypt( blockify( bytes( pt ), block_size ), cipher, nonce )
		
		new_ct = b''.join( [ b for b in new_cipherblocks ] )
		ciphertexts.append( new_ct )

	return ciphertexts


cipher = AES.new( b'ABCDEFGHIJKLMNOP', AES.MODE_ECB )
ct = encryptor( cipher )

crack( ct )










