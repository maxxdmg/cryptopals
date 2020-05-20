hexbuff1 = "1c0111001f010100061a024b53535009181c"
hexbuff2 = "686974207468652062756c6c277320657965"
result = ""

for i in range(len(hexbuff1)):
	b1 = bin(int(hexbuff1[i],16))[2:].zfill(4)
	b2 = bin(int(hexbuff2[i],16))[2:].zfill(4)
	result += str(hex( int(b1,2) ^ int(b2,2) )[2:])

answer = "746865206b696420646f6e277420706c6179"
if (result == answer):
	print("works!")

