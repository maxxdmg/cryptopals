def fixed_xor (x, y):
	# get int values for x & y
	x = int(x, 16)
	y = int(y, 16)
	# xor the int values then return as hex
	return hex(x ^ y)

print(fixed_xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965"))