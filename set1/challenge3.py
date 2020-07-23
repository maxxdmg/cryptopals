'''
Single-byte XOR cipher
'''
#def get_next_max()

def single_byte_xor(a, b):
	ret = bytearray()
	tar = a; key = b;

	for i in range( len( tar ) ):
		new_value = ord( tar[ i ] ) ^ key
		ret.append( new_value )
	return bytes(ret)


def calc_freq( s ):
	etao = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
	frequencies = {}
	minctr = -1

	for ch in s:
		if ch in frequencies:
			frequencies[ ch ] += 1
			
			if frequencies[ ch ] < minctr or minctr < 0:
				minctr = frequencies[ ch ]
		else:
			frequencies[ ch ] = 1
	
	score = 0
	for ch in frequencies:
		c = chr( ch )
		if c in etao.lower() or c in etao:
			score += 1
	return score


ct = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

ct = bytes.fromhex( ct ).decode( 'utf-8' )

keychar = (-1, '')
for i in range( 10,256,1 ):
	possible_pt = single_byte_xor( ct, i )

	score = calc_freq(possible_pt)

	if score > keychar[ 0 ] or keychar[ 0 ] < 0:
		keychar = ( score, chr(i) )
		
print(single_byte_xor( ct, ord(keychar[1]) ) )