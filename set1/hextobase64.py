import base64

def hex_to_base64 (x):
	# Decode hex
	hex_str = bytes.fromhex(x)
	# Encode decoded hex string
	base64_str = base64.b64encode(hex_str)
	return base64_str.decode()

print(hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6dcd"))