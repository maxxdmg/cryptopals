table = {
	"0":"A",
	"1":"B",
	"2":"C",
	"3":"D",
	"4":"E",
	"5":"F",
	"6":"G",
	"7":"H",
	"8":"I",
	"9":"J",
	"10":"K",
	"11":"L",
	"12":"M",
	"13":"N",
	"14":"O",
	"15":"P",
	"16":"Q",
	"17":"R",
	"18":"S",
	"19":"T",
	"20":"U",
	"21":"V",
	"22":"W",
	"23":"X",
	"24":"Y",
	"25":"Z",
	"26":"a",
	"27":"b",
	"28":"c",
	"29":"d",
	"30":"e",
	"31":"f",
	"32":"g",
	"33":"h",
	"34":"i",
	"35":"j",
	"36":"k",
	"37":"l",
	"38":"m",
	"39":"n",
	"40":"o",
	"41":"p",
	"42":"q",
	"43":"r",
	"44":"s",
	"45":"t",
	"46":"u",
	"47":"v",
	"48":"w",
	"49":"x",
	"50":"y",
	"51":"z",
	"52":"0",
	"53":"1",
	"54":"2",
	"55":"3",
	"56":"4",
	"57":"5",
	"58":"6",
	"59":"7",
	"60":"8",
	"61":"9",
	"62":"+",
	"63":"/"
}

plaintext = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

bin_string = "".join( [bin(int(ch,16))[2:].zfill(4) for ch in plaintext] )

block_size = 6
length = len(bin_string)
blocks = length // block_size

result = ""

for i in range(blocks):
	new_ch = bin_string[i*6:i*6 + 6]
	result += table[str(int(new_ch,2))]

answer = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
if (result == answer):
	print("works!")