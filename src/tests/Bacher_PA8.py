"""Programming Assignment 8: AES-128 Encryption
50 minutes | 25 points

Name: Seth Bacher
Complete the FOUR functions below. Record answers to Questions 1-7
on the worksheet. Do not modify the supplied constants or helper functions.
Submit this completed Python file and your worksheet via Canvas.
"""

# AES-128 encrypts 16-byte blocks using a 16-byte key.
# Each byte is represented by a decimal integer from 0 to 255.
# The 16-byte state is stored COLUMN BY COLUMN (not row by row):
#
#     row 0: state[0]  state[4]  state[8]  state[12]
#     row 1: state[1]  state[5]  state[9]  state[13]
#     row 2: state[2]  state[6]  state[10] state[14]
#     row 3: state[3]  state[7]  state[11] state[15]
#
# Element at row r, column c is at index 4*c + r.
# Each column comprises four consecutive elements of the Python list.

#SBOX and RCON (AES round constants) are provided as decimal integers.
SBOX = [
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22,
]
RCON = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]

#Hex-byte conversion functions
def hex_to_bytes(text):
    """Convert a hex string to a list of decimal byte integers (0-255)."""
    return list(bytes.fromhex(text))

def bytes_to_hex(values):
    """Convert a list of decimal byte integers to uppercase hexadecimal text."""
    return ''.join(f'{value:02X}' for value in values)

# ============================================================
# PART 1: ADDROUNDKEY (4 points)
# ============================================================

#Implement AddRoundKey. Return a new list of 16 integers, XORing corresponding bytes.
def add_round_key(state, round_key):
    #INSERT YOUR CODE HERE
    output_xor = []
    for i in range(0,16):
        output_xor.append(state[i]^round_key[i])

    return output_xor


# ============================================================
# PART 2: SUBBYTES (5 points)
# ============================================================

#Implement SubBytes. Use SBOX to substitute all 16 state bytes. Return a new list.
def sub_bytes(state):
    #INSERT YOUR CODE HERE
    output_sb = []
    for i in range(0,16):
        output_sb.append(SBOX[state[i]])

    return output_sb


# ============================================================
# PART 3: SHIFTROWS (5 points)
# ============================================================

#Implement ShiftRows. Return a new list of 16 integers.
def shift_rows(state):
    #INSERT YOUR CODE HERE
    output_shift = []
    for i in range(0,16,4):
        output_shift.append(state[i])
        output_shift.append(state[(i+5)%16])
        output_shift.append(state[(i+10)%16])
        output_shift.append(state[(i+15)%16])
    return output_shift


# ============================================================
# PART 4: MIXCOLUMNS (6 points)
# ============================================================
# These multiplication helper functions can be used in your mix_columns() function. Do not modify them!
def multiply_by_02(a):
    """Multiply byte a by 02 in AES GF(2^8)."""
    return ((a << 1) ^ (27 if a & 128 else 0)) & 255
def multiply_by_03(a):
    """Multiply byte a by 03 in AES GF(2^8)."""
    return multiply_by_02(a) ^ a

#Implement MixColumns. Return a new list of 16 integers.
def mix_columns(state):
    #INSERT YOUR CODE HERE
    output_mixed = []
    mult = [2,1,1,3,3,2,1,1,1,3,2,1,1,1,3,2]
    for i in range(0,16):
        if mult[i] == 1:
            output_mixed.append(state[i])
        elif mult[i] == 2:
            output_mixed.append(multiply_by_02(state[i]))
        elif mult[i] == 3:
            output_mixed.append(multiply_by_03(state[i]))
    return output_mixed


# ============================================================
# PART 5: AES ENCRYPTION (5 points) - PROVIDED CODE
# ============================================================
def aes_round_keys(key):
    """Provided AES-128 key expansion: 11 round keys of 16 bytes."""
    words = [key[i:i+4] for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = words[i-1].copy()
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]       # RotWord
            temp = [SBOX[b] for b in temp]   # SubWord
            temp[0] ^= RCON[i//4 - 1]
        words.append([words[i-4][j] ^ temp[j] for j in range(4)])
    return [sum(words[4*r:4*r+4], []) for r in range(11)]

def aes_encrypt_block(plaintext, key):
    """Provided AES-128 single-block encryption using student functions."""
    round_keys = aes_round_keys(key)
    state = add_round_key(plaintext, round_keys[0])
    for round_number in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round_number])
    # Final AES round has NO MixColumns.
    state = sub_bytes(state)
    state = shift_rows(state)
    return add_round_key(state, round_keys[10])


# ============================================================
# WORKSHEET TEST CASES - RUN AFTER IMPLEMENTING YOUR FUNCTIONS
# ============================================================
# Question 1:
q1_state = [0, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187, 204, 221, 238, 255]
q1_key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
print('Question 1:', add_round_key(q1_state, q1_key))

# Question 2: Use SBOX to look up input byte 123. Record the decimal result on your worksheet.
print('Question 2:', SBOX[123])

# Question 3:
q3_state = [8, 6, 7, 5, 3, 0, 9, 8, 6, 7, 5, 3, 0, 9, 8, 6]
print('Question 3:', sub_bytes(q3_state))

# Question 4: Written question on confusion versus diffusion.

# Question 5:
q5_state = [10, 20, 15, 5, 50, 100, 86, 75, 30, 9, 8, 7, 6, 5, 4, 3]
print('Question 5:', shift_rows(q5_state))

# Question 6:
q6_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
print('Question 6:', mix_columns(q6_state))

# Question 7:
plain = hex_to_bytes('00112233445566778899AABBCCDDEEFF')
key = hex_to_bytes('000102030405060708090A0B0C0D0E0F')
# Complete Parts 1-4 before uncommenting the following lines:
ciphertext = aes_encrypt_block(plain, key)
print('Question 7:', bytes_to_hex(ciphertext))