from Crypto.Cipher import AES

f = open("8.txt")
ciphertext = [bytes.fromhex(line.strip()) for line in open('8.txt')]
# block size was given in challenge desc yooo
block_size = 16

index = 0
for cipher in ciphertext:
	chunks = [cipher[i:i+block_size] for i in range(0, len(cipher), block_size)]
	if len(chunks) - len(set(chunks)) != 0:
		print(index)

	index+=1
