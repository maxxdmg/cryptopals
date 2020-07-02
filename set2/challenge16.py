from Crypto.Cipher import AES
from challenge14 import cbc_encrypt, cbc_decrypt, pad_pcks7, generate_key
from challenge15 import validate_pcks7

def bytescpy (dest, src):
	for b in src:
		dest.append( b )
	return dest

def sanitize (x):
	x = x.replace(';', '')
	return x.replace('=', '')

def parse (usertext):
	if type(usertext) == bytes:
		usertext = usertext.decode('utf-8')

	ret = "comment1=cooking%20MCs;userdata="
	ret += usertext
	ret += ";comment2=%20like%20a%20pound%20of%20bacon"

	return pad_pcks7( bytes( sanitize( ret ), 'utf-8' ), 16 )

def encrypt (text, key, iv):
	cipher = AES.new( key, AES.MODE_ECB )
	return cbc_encrypt( parse( text ), iv, cipher )

def decrypt (text, key, iv):
	cipher = AES.new( key, AES.MODE_ECB )
	plaintext = b''.join( [ plainblock for plainblock in cbc_decrypt( text, iv, cipher ) ] )
	plaintext = validate_pcks7( plaintext, 16 )
	data = plaintext.split(b';')
	for item in data:
		if b'admin=true' in item:
			return True
	return False

def main ():
	key = generate_key()
	iv = generate_key()

	# attacker controlled input
	userinput = 'hello world!adminXtrue'

	cipherblocks = encrypt( userinput , key, iv )
	for targetblock in range( len(cipherblocks) ):
		for targetindex in range( 16 ):
			for i in range(256):
				maliciousblock = bytescpy( bytearray(), cipherblocks[targetblock] )
				maliciousblock[targetindex] = i
				
				payload = []
				for block in cipherblocks:
					payload.append( bytes( bytescpy( bytearray(), block ) ))
				payload[targetblock] = bytes(maliciousblock)

				result = decrypt( payload, key, iv )
				if result == True:
					print( "ADMIN ACCESS ACHIEVED!" )
					return

main()

