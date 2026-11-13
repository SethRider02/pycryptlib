"""
Crypto Exercise 3: Stream Ciphers, XOR and One-Time Pads

Complete each TODO. Do not delete the function names or test cases.
Submit your completed .py file and Worksheet to Canvas.
"""

#Import Python secrets module for random bit generation.
import secrets

# -----------------------------------------------------------------------------
# PROVIDED HELPER FUNCTIONS
# These functions convert between text and lists of bits.
# WARNING: DO NOT MODIFY.
# -----------------------------------------------------------------------------

def text_to_bits(text):
    """Encode a string as UTF-8 and return its bits as a list of 0s and 1s."""
    return [
        (byte >> shift) & 1
        for byte in text.encode("utf-8")
        for shift in range(7, -1, -1)
    ]

def bits_to_text(bits):
    """Convert a bit list whose length is a multiple of 8 back into text."""
    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be a multiple of 8.")

    byte_values = []
    for start in range(0, len(bits), 8):
        value = 0
        for bit in bits[start:start + 8]:
            value = (value << 1) | bit
        byte_values.append(value)

    return bytes(byte_values).decode("utf-8")

# -----------------------------------------------------------------------------
# PART 1: XOR BIT LISTS
# -----------------------------------------------------------------------------

"""XOR two equal-length lists containing only 0s and 1s."""
def xor_bits(data_bits, keystream_bits):
    #Checks to make sure data_bits and keystream_bits are the same length AND that they only contain 0s and 1s.
    if len(data_bits) != len(keystream_bits):
        raise ValueError("Data and keystream must have the same length.")
    if not all(bit in (0, 1) for bit in data_bits + keystream_bits):
        raise ValueError("Data and keystream must contain only 0s and 1s.")

    # TODO: INSERT YOUR CODE HERE
    i = 0
    cipherbits = []
    while i < len(data_bits):
        if data_bits[i] != keystream_bits[i]:
            cipherbits.append(1)
        else:
            cipherbits.append(0)
        i = i+1

    #Replace 'return None' with your output list of bits following the XOR operation.
    return cipherbits

# -----------------------------------------------------------------------------
# PART 2: GENERATE A ONE-TIME PAD
# Python secrets module is designed for security-sensitive random values.
# Hint: secrets.randbits(1) returns one random bit (either 0 or 1).
# -----------------------------------------------------------------------------

"""Return a new list containing random bits of the specified length."""
def generate_one_time_pad(length):
    #Input validation: checks to make sure the length is non-negative
    if length < 0:
        raise ValueError("Length cannot be negative.")

    # TODO: INSERT YOUR CODE HERE
    i = 0
    rand_pad = []
    while i < length:
        rand_pad.append(secrets.randbits(1))
        i = i+1
    #Replace 'return None' with your list of bits representing a one-time pad for the specified length.
    return rand_pad

# -----------------------------------------------------------------------------
# PART 3: ENCRYPTION AND DECRYPTION
# Encryption: ciphertext bits = plaintext bits XOR pad bits
# Decryption: plaintext bits = ciphertext bits XOR the SAME pad bits
# -----------------------------------------------------------------------------

def otp_encrypt(plaintext):
    """
    Complete the following steps:
    1. Convert plaintext string input to a list of bits using the provided helper function called text_to_bits(text)
    2. Generate a one-time pad using your existing generate_one_time_pad(length) function and STORE THE RESULT AS A VARIABLE
    3. XOR the list of bits representing the plaintext with the one-time pad using your existing xor_bits(data_bits, keystream_bits) function
    4. Return both the ciphertext bit list and the one-time pad used for encryption as a Python tuple, i.e. return (ciphertext list,one-time pad)"""

    # TODO: INSERT YOUR CODE HERE
    bit_text = text_to_bits(plaintext)
    ot_pad = generate_one_time_pad(len(bit_text))
    cbit_text = xor_bits(bit_text, ot_pad)
    #Replace 'return None' with a tuple containing your output ciphertext bit list and the one-time pad used for encryption (the OTP should be a list of bits)
    return (cbit_text,ot_pad)


def otp_decrypt(ciphertext_bits, otp):
    """XOR the ciphertext bit list with the one-time pad (keystream) used to encrypt the ciphertext, and convert the resulting bit list back to an ASCII plaintext string.
    """

    # TODO: INSERT YOUR CODE HERE
    pbit_text = xor_bits(ciphertext_bits,otp)
    #Replace 'return None' with your output plaintext ASCII string.
    return bits_to_text(pbit_text)


# -----------------------------------------------------------------------------
# TEST AREA
# Run this file often as you work.
# -----------------------------------------------------------------------------

print("PART 1: XOR BIT LISTS")
plaintext_bits = [0, 1, 0, 0, 0, 0, 0, 1]  # ASCII A
keystream_bits =  [0, 0, 1, 0, 1, 0, 1, 0]
result_1 = xor_bits(plaintext_bits, keystream_bits)
print("1. Ciphertext Bit List:", result_1)
result_2 = xor_bits(result_1, keystream_bits)
print("2. Recovered Plaintext Bit List:", result_2)


print("PART 2: GENERATE A ONE-TIME PAD")
first_pad = generate_one_time_pad(16)
second_pad = generate_one_time_pad(16)
print("4. First 16-bit pad: ", first_pad)
print("5. Second 16-bit pad:", second_pad)
print("Are the one-time pads different? Answer:", first_pad != second_pad)

print("PART 3: ENCRYPT AND DECRYPT")
go_bears_bits = text_to_bits("GO BEARS!")
print("7. Number of bits in output list is:",len(go_bears_bits))
#Write line of code to print the length of the go_bears_bits list.

encrypt_otp = otp_encrypt("CGA")
print("8. Ciphertext ASCII string output and corresponding one-time pad is:", encrypt_otp)
print("9. Decrypted ASCII plaintext is:",otp_decrypt(encrypt_otp[0],encrypt_otp[1]))
#Write line of code to print the decrypted ASCII plaintext string using your otp_decrypt function. The function should take your results from Question 8 as inputs.