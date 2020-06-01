from Crypto.Cipher import AES
from random import randrange
import base64

def pad_pcks7(ciphertext,size):
	if len(ciphertext) % size == 0:
		return ciphertext

	ret = bytearray()
	for b in ciphertext:
		ret.append(b)
	
	remainder = size - (len(ciphertext) % size)

	for pad in range(remainder):
		ret.append(remainder)
	return bytes(ret)

def decode_object(string, assign_symbol, and_symbol):
	parsed_object = {}

	items = string.split(and_symbol)
	for item in items:
		values = item.split(assign_symbol)
		parsed_object[values[0]] = values[1]

	return parsed_object

def encode_object(obj, assign_symbol, and_symbol):
	parsed_object = ""

	first_loop = True

	for item in obj:
		if not first_loop:
			parsed_object += and_symbol
		parsed_object += str(item) + assign_symbol + str(obj[item])
		first_loop = False

	return parsed_object

def generate_key():
	ret = bytearray()
	for i in range(16):
		ret.append( randrange(64,128) )
	return bytes(ret)

def encrypt_profile(plainblocks, key):
	cipherblocks = []
	cipher = AES.new(key, AES.MODE_ECB)
	for block in plainblocks:
		cipherblocks.append(cipher.encrypt(pad_pcks7(block,16)))
	return cipherblocks

def decrypt_profile(cipherblocks, key):
	plainblocks = []
	cipher = AES.new(key, AES.MODE_ECB)
	for block in cipherblocks:
		plainblocks.append(cipher.decrypt(block))
	return plainblocks

def profile_for(email, uid):
	bad_chars = ["&","="]
	for char in bad_chars:
		email = email.replace(char, '')

	profile = {}
	profile["email"] = email
	profile["uid"] = uid
	profile["role"] = 'user'

	return encode_object(profile, "=", "&")

size = 16
profile = profile_for("aaaaaaaaaaaaa", 10)
# split encoding text into blocks -> this would be our action
profile_blocks = [bytes(profile[i:i+size],"utf-8") for i in range(0,len(profile),size)]

payload = profile_for("aaaaaaaaaa", 11)
payload_blocks = [bytes(payload[i:i+size],"utf-8") for i in range(0,len(payload),size)]
# we need to craft a malicious block, this will be the text admin but must also occupy an entire block space so we pad it
new_payload_block = pad_pcks7(bytes("admin","utf-8"),size)
# place the newly crafted admin block into the payload blocks so it can be encrypted
temp_blocks = payload_blocks
payload_blocks = [temp_blocks[0], new_payload_block]
# add the rest of the temp blocks to our new payload block list
for i in range(1,len(temp_blocks),1):
	payload_blocks.append(temp_blocks[i])

# submit the payload and regular profile for encryption
key = generate_key() # unknown to attacker
# encrypt profile
cipherblocks = encrypt_profile(profile_blocks,key) # would be obtained and known by attacker

# encrypt payload
payload_cipherblocks = encrypt_profile(payload_blocks,key)

# our malicious block will be in position 1 of the payload encryption block list
# the target block to be replaced with the malicious block will be the last block in the cipherblocks list
malicious = 1
target = len(cipherblocks)-1
cipherblocks[target] = payload_cipherblocks[malicious]

plainblocks = decrypt_profile(cipherblocks,key) # would not be known but could be assumed


# remove any padding off the final block
depad = plainblocks[len(plainblocks) - 1][size-1]
depad_block = bytearray()
if depad<size:
	for i in range(size - depad):
		next_byte = plainblocks[len(plainblocks) - 1][i]
		depad_block.append(next_byte)
	plainblocks[len(plainblocks) - 1] = bytes(depad_block)

# combine the array of byte objects
plaintext = ""
for block in plainblocks:
	for b in block:
		plaintext += chr(b)

# will now output the profile encoded with the role of admin
print(plaintext)