def get_english_score(input_bytes):
    freq = {
    	'a': 1, 'b': 1, 'c': 1, 'd': 1,
        'e': 1, 'f': 1, 'g': 1, 'h': 1,
        'i': 1, 'j': 1, 'k': 1, 'l': 1,
        'm': 1, 'n': 1, 'o': 1, 'p': 1,
        'q': 1, 'r': 1, 's': 1, 't': 1,
        'u': 1, 'v': 1, 'w': 1, 'x': 1,
        'y': 1, 'z': 1, ' ': 1
    }

    return sum([freq.get(chr(byte), 0) for byte in input_bytes.lower()])


def single_char_xor(input_bytes, char_value):
    ret = b''
    for byte in input_bytes:
        ret += bytes([byte ^ char_value])
    return ret


def bruteforce_single_char_xor(ciphertext):
    """Performs a singlechar xor for each possible value(0,255), and
    assigns a score based on character frequency. Returns the result
    with the highest score.
    """
    potential_messages = []
    for key_value in range(256):
        message = single_char_xor(ciphertext, key_value)
        score = get_english_score(message)
        data = {
            'message': message,
            'score': score,
            'key': key_value
            }
        potential_messages.append(data)
    return sorted(potential_messages, key=lambda x: x['score'], reverse=True)[0]


def main():
    ciphers = open('challenge4.txt').read().splitlines()
    potential_plaintext = []
    for hexstring in ciphers:
        ciphertext = bytes.fromhex(hexstring)
        potential_plaintext.append(bruteforce_single_char_xor(ciphertext))
    best_score = sorted(potential_plaintext, key=lambda x: x['score'], reverse=True)[0]
    for item in best_score:
        print("{}: {}".format(item.title(), best_score[item]))
        

if __name__ == '__main__':
    main()