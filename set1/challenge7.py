import base64 as b64
from Crypto.Cipher import AES

f = open("challenge7.txt")
ciphertext = b64.b64decode("".join( [line.strip() for line in f] ) )
# the key was given in the challenge, same as the ciphertext
key = "YELLOW SUBMARINE"

cryptsys = AES.new(key, AES.MODE_ECB)
plaintext = cryptsys.decrypt(ciphertext)
print(plaintext) 
