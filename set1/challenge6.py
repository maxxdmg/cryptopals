from base64 import b64decode

def hamming_distance( x, y ):
	ret = 0
	for b1, b2 in zip( x, y ):
		ret += bin( b1 ^ b2 ).count('1')
	return ret

def get_possible_keysizes( ciphertext ):
	avg_distances = []

	for keysize in range( 2, 40, 1 ):
		chunks = [ ciphertext[i:i+keysize] for i in range( 0, len(ciphertext), keysize ) ]
		distances = []

		for i in range( len(chunks)-1 ):
			normalized_dist = hamming_distance( chunks[i], chunks[i+1] ) / keysize
			distances.append(normalized_dist)

		result = {
			'keysize':keysize,
			'dist': sum( distances ) / len( distances )
		}

		avg_distances.append( result )

	return sorted( avg_distances, key=lambda x: x['dist'] )

def blockify( ciphertext, size ):
	return [ ciphertext[ i:i+size ] for i in range( 0, len(ciphertext), size ) ]


def transpose( blocks, keysize ):
	result = []
	for i in range( keysize ):
		new_block = bytearray()
		for block in blocks:
			try:
				new_block.append( block[i] )
			except:
				break
		result.append( bytes( new_block ) )
	return result

def untranspose( blocks, keysize ):
	result = []
	for block in blocks:
		new_block = bytearray()
		for i in range( keysize ):
			try:
				new_block.append( block[i] )
			except:
				break
		result.append( bytes( new_block ) )
	return result


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


def bruteforce_single_char_xor(ciphertext):
    potential_messages = []
    for key_value in range(256):
        message = single_char_xor(ciphertext, key_value)
        score = get_english_score(message)
        data = {
            'message': message,
            'score': score,
            'key': key_value
            }
        potential_messages.append(data)
    return sorted(potential_messages, key=lambda x: x['score'], reverse=True)[0]
ct = b''

f = open( "challenge6.txt" )
for line in f:
	 ct += b64decode( line.strip( '\n' ) )

keysizes = get_possible_keysizes( ct )
keysize = keysizes[0]['keysize']

cblocks = blockify( ct, keysize )

tblocks = transpose( cblocks, keysize )

cracked_blocks = [ bruteforce_single_char_xor( block ) for block in tblocks ]

key = b''
pt = []
for data in cracked_blocks:
	key += bytes(chr(data['key']),'utf-8')
print(key)
