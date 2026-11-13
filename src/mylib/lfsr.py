# Contains various functions dealing with Linear Feedback Shift Registers (LFSR's)

def text_to_bits(text):
    """Convert uppercase A-Z text into one flat list of 5-bit values."""
    bits = []
    for char in text:
        value = ord(char) - ord("A")
        if value < 0 or value > 25:
            raise ValueError("Only uppercase letters A-Z are allowed.")
        bits.extend([
            (value >> 4) & 1,
            (value >> 3) & 1,
            (value >> 2) & 1,
            (value >> 1) & 1,
            value & 1
        ])
    return bits


def bits_to_text(bits):
    """Convert a flat list of 5-bit letter values back into uppercase text."""
    if len(bits) % 5 != 0:
        raise ValueError("The number of bits must be a multiple of 5.")

    text = ""
    for i in range(0, len(bits), 5):
        group = bits[i:i + 5]
        value = (
            group[0] * 16 + group[1] * 8 + group[2] * 4
            + group[3] * 2 + group[4]
        )
        if value > 25:
            raise ValueError("5-bit value does not represent A-Z.")
        text += chr(value + ord("A"))
    return text


def clock_lfsr(seed, clocks):
    """Shifts a 5-bit seed 'clocks' amount of clock cycles. Returns shifted bits as a list."""
    cipher = []
    for i in range(len(seed)):
        cipher.append(seed[i])

    for i in range(clocks):
        tempbit = (cipher[2] + cipher[0]) % 2
        cipher.append(tempbit)
        cipher.pop(0)

    
    return cipher


def lfsr(seed, length):
    """Generates a key of a specified length given a seed. Returns the keystream as a list of bits."""
    keystream = []
    for i in range(len(seed)):
        keystream.append(seed[i])

    for i in range(5,length):
        tempbit = (keystream[i-5] + keystream[i-3]) % 2
        keystream.append(tempbit)

    return keystream


def lfsr_encrypt(plaintext, seed):
    """Encrypts a string plaintext with a seed list of five bits. Returns tuple with ciphertext as a list
     of bits and keystream as a list of bits."""
    plainbits = text_to_bits(plaintext)
    cipherbits = []
    keystream = lfsr(seed,(len(plainbits)))

    for i in range(0,len(plainbits)):
        tempbit = (plainbits[i] + keystream[i]) % 2
        cipherbits.append(tempbit)

    return (cipherbits,keystream)


def lfsr_decrypt(ciphertext_bits, keystream):
    """Decrypts a list of ciphertext bits using a keystream list of bits. Returns a string of text."""
    plainbits = []
    for i in range(0,len(ciphertext_bits)):
        tempbit = (ciphertext_bits[i] + keystream[i]) % 2
        plainbits.append(tempbit)

    plaintext = bits_to_text(plainbits)

    return plaintext
