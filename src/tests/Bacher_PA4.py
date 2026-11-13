"""
Crypto Exercise 4: Linear Feedback Shift Registers (LFSRs)
50 minutes | 20 points

Name: FIRST AND LAST NAME
"""

# ============================================================
# PROVIDED HELPER FUNCTIONS (DO NOT EDIT!)
# ============================================================
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

# ============================================================
# PART 1 - LFSR CLOCKS
# ============================================================

#The below function should complete 'clocks' clocks of the LFSR and return the final register state (list of 5 bits).
def clock_lfsr(seed, clocks):

    #INSERT YOUR CODE HERE
    cipher = []
    for i in range(len(seed)):
        cipher.append(seed[i])

    for i in range(clocks):
        tempbit = (cipher[2] + cipher[0]) % 2
        cipher.append(tempbit)
        cipher.pop(0)

    
    return cipher  #Replace 'None' with the final register state (a list of 5 bits) after 'clocks' clocks.


## Worksheet Questions - Part 1:
print('PART 1:')
seed = [1, 0, 0, 0, 1]

#Question 1:
reg_state = clock_lfsr(seed,1)
print("1. The new bit is: ", reg_state[4])

#Question 2:
print("2. State after 4 clocks:", clock_lfsr(seed, 4))

# Question 3:
# TODO: Write a loop that tests increasing numbers of clocks until clock_lfsr(seed, clocks) returns to the original seed.
clocks = 0
# INSERT LOOP which increments 'clocks' and runs clock_lfsr(seed, clocks) until the LFSR returns to the original seed.
test_seed = []
while(seed != test_seed):
    clocks += 1
    test_seed = clock_lfsr(seed, clocks)
print("3. The LFSR returns to the original seed after", clocks, "clocks.")


# ============================================================
# PART 2 - LFSR KEYSTREAM GENERATION
# ============================================================

#The function below should generate a keystream of the specified length using the LFSR with the given seed.
def lfsr(seed, length):

    #INSERT YOUR CODE HERE
    keystream = []
    for i in range(len(seed)):
        keystream.append(seed[i])

    for i in range(5,length):
        tempbit = (keystream[i-5] + keystream[i-3]) % 2
        keystream.append(tempbit)

    return keystream #Replace 'None' with the final keystream (a list of bits)

## Worksheet Questions - Part 2:
print('PART 2:')
seed_2 = [1,0,1,0,1]

#Question 4:
print("4. The first 10 bits of the keystream are:", lfsr(seed_2, 10))

#Question 5:
keystream_62 = lfsr(seed_2, 62)
print("62-bit keystream:", keystream_62)
print("Bits 1-31: ", keystream_62[:31])
print("Bits 32-62:", keystream_62[31:62])

#Question 6:
bad_seed = [0,0,0,0,0]
print("Example of keystream with a bad seed:", lfsr(bad_seed, 10))


# ============================================================
# PART 3 - LFSR ENCRYPTION AND DECRYPTION
# ============================================================

#The below function should take a plaintext string of letters and a seed, and return a tuple containing the ciphertext bits and the keystream used for encryption.
def lfsr_encrypt(plaintext, seed):
    
    #INSERT YOUR CODE HERE
    plainbits = text_to_bits(plaintext)
    cipherbits = []
    keystream = lfsr(seed,(len(plainbits)))

    for i in range(0,len(plainbits)):
        tempbit = (plainbits[i] + keystream[i]) % 2
        cipherbits.append(tempbit)

    return (cipherbits,keystream) #Replace 'None' with a tuple containing the ciphertext bits and the keystream used for encryption.


def lfsr_decrypt(ciphertext_bits, keystream):

    #INSERT YOUR CODE HERE
    plainbits = []
    for i in range(0,len(ciphertext_bits)):
        tempbit = (ciphertext_bits[i] + keystream[i]) % 2
        plainbits.append(tempbit)

    plaintext = bits_to_text(plainbits)

    return plaintext #Replace 'None' with the recovered plaintext string.

## Worksheet Questions - Part 3:
seed_3 = [1,0,0,0,1]
print("PART 3:")

#Question 7:
ciphertext, keystream = lfsr_encrypt("ACADEMY", seed_3)
print("7. Ciphertext bits:", ciphertext)
print("7. Keystream:", keystream)

#Question 8:
ciphertext_8 = [0,1,0,0,0, 0,1,0,1,0, 1,0,0,1,0, 1,1,0,0,1, 0,1,1,1,1, 0,1,0,1,0, 1,1,0,1,0, 0,1,0,0,0, 1,0,1,1,0, 0,0,1,0,0, 1,0,0,0,1, 1,0,0,0,1, 0,0,1,1,1, 0,0,1,1,1, 0,1,0,1,0]
keystream_8 = [0,0,1,0,0, 0,0,0,1,0, 0,0,0,0,0, 0,1,0,1,1, 0,0,1,1,1, 0,0,1,0,0, 1,0,1,1,1, 0,1,0,1,0, 1,1,0,0,0, 0,1,0,0,0, 1,1,1,1,0, 1,1,0,1,0, 0,0,0,1,1, 1,0,1,0,0, 0,1,1,1,0]
 
recovered_plaintext = lfsr_decrypt(ciphertext_8, keystream_8)
print("8. Plaintext:", recovered_plaintext)