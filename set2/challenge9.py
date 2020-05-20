def pad(s, n):
	ret = s
	padding = n - len(s)
	for i in range(0,padding,1):
		ret += '\\x' + hex(padding)[2:].zfill(2)
	return ret
plaintext="YELLOW SUBMARINE"
print(pad(plaintext, 20))
