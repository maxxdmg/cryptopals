from Crypto.Cipher import AES
from random import randrange
import base64

def concat_bytes(a,b):
	ret = bytearray()
	for byte in a:
		ret.append(byte)
	for byte in b:
		ret.append(byte)
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
		ret.append(xor(cipher.decrypt(c), prev_block))
		prev_block = c
	return ret

def generate_key():
	ret = bytearray()
	for i in range(16):
		ret.append( randrange(64,128) )
	return bytes(ret)

def find_block_size(ciphertext,key, iv):
	length = len(ciphertext)
	i = 1
	while 1:
		data = bytearray("A" * i, "utf-8")
		new_length = unknown_encrypt(bytes(data), key, iv)
		if len(new_length) !=  length:
			return len(new_length) - length
		i+=1

iv = b'EeA@^zj]tiOhL^@`' # same context as below 
key = b'kSD|ibaTqUxd`CPi' # randomly generated at some point
cryptsys = AES.new(key, AES.MODE_ECB)

size = 16#find_block_size(key, iv)

mytext = bytes("".join(["A" for i in range(0,size,1)]), "utf-8")

unknowntext = base64.b64decode(bytearray("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK","utf-8"))

ciphersys = AES.new(key, AES.MODE_ECB)

targettext = pad_pcks7(concat_bytes(mytext,unknowntext),size)
# slice bytes objects into blocks
plainblocks = [bytes(targettext[i:i+size]) for i in range(0,len(targettext),size)]
cipherblocks = cbc_encrypt(plainblocks,iv,ciphersys)
# will be used as a decryption tool
dictionary = dict()

decrypted = b''


# create our controlled input
new_payload = bytearray()
block = len(unknowntext) // 16

for j in range(0,size*(block+1),1):
	new_payload.append(ord("A"))

for loop in range(0,size*(block+1),1):
	for i in range(0,256):
		new_payload[len(new_payload)-1] = i # the last byte in the payload is the test byte that will be the new decrypted character
		# concat & pad our controlled input and the unknown text
		targettext = pad_pcks7(concat_bytes(bytes(new_payload),unknowntext), size)
		# slice bytes objects into blocks
		plainblocks = [bytes(targettext[i:i+size]) for i in range(0,len(targettext),size)] # chop the text into length 16 blocks -> cbc requires blocks
		# swap block spots
		cipherblocks = cbc_encrypt(plainblocks,iv,ciphersys)
		# append to decryption dictionary
		dictionary[cipherblocks[block]]=bytes(new_payload[:size*(block+1)]) # add the nth block to a dictionary where n is the current block being cracked
	# reduce the number of controlled characters every loop (1st loop:AAAA,2nd loop:AAA,3rd loop:AA, etc...)
	mytext = bytes(new_payload[0:size*(block+1)-loop])

	# targettext = mytext + unknowntext
	targettext = pad_pcks7(concat_bytes(mytext,unknowntext),size)
	# slice again into blocks (NOTE important because cbc)
	plainblocks = [bytes(targettext[i:i+size]) for i in range(0,len(targettext),size)]
	cipherblocks = cbc_encrypt(plainblocks,iv,ciphersys)
	
	# this break condition just works, found thru trial and error
	if(len(b''.join(cipherblocks)) == size*(block+1)):
		break
	else:
		print((loop+1) / size*(block+1))

	decrypted = dictionary[cipherblocks[block]] # set the new potential full decrypted string to the value in the dictionary
	new_payload = bytearray()
	for b in dictionary[cipherblocks[block]]:
		new_payload.append(b)
	#print(plainblocks)
	
	# remove the first element, to be able to decrypt the next unknown text byte (first element will always be your provided text)
	new_payload = new_payload[1:]
	# append a changeable character that will be the manipulated byte
	new_payload.append(ord("A"))

print(decrypted[size*(block+1)-loop+1:])

exit(0)

'''
old shit here yo
'''
ecb = False
for cipher in cipherblocks:
	if ( len(cipher) - len(set(cipher)) != 0):
		ecb = True
		break
print(ecb)
