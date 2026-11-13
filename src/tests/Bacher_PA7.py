"""Programming Assignment 7: DES Permutations, S-Boxes & Feistel Function.
50 minutes | 20 points

Name: 2/c Seth Bacher
Complete the functions and exercises below. Record answers to
Questions 1-8 on the worksheet. Do not change provided function names or tables.
"""

# Standard DES tables
IP = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]
E = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]
P = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]
PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
]
PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Each S-box contains four rows of 16 integers (0-15)
SBOXES = [
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]
#Useful helper functions
def hex_to_bits(hex_string, width=64):
    """Given hexadecimal text, return exactly width binary characters."""
    return format(int(hex_string, 16), f"0{width}b")

def bits_to_hex(bits):
    """Given binary text, return uppercase hexadecimal text (with leading zeros)."""
    return format(int(bits, 2), f"0{len(bits) // 4}X")

def xor_bits(left, right):
    """Provided helper: bitwise XOR of two equal-length binary strings."""
    return ''.join('1' if a != b else '0' for a, b in zip(left, right))


# ============================================================
# PART 1: BIT PERMUTATIONS (5 points)
# ============================================================
def permute(bits, table):
    """Return bits reordered using the given permutation table."""
    output = ""
    for index in table:
        output = f"{output}{bits[index-1:index]}"
    return output  # Replace None with the correct bit string.


# Question 1: Apply a short sample permutation.
print('Question 1:')
print('Permuted bits =', permute('10110010', [2, 4, 6, 8]))
# Question 2: What adjustment is needed for Python string indexing?
# Answer on your worksheet.
# Question 3: How many output bits do E and PC-1 produce?
# Answer on your worksheet.


# ============================================================
# PART 2: DES S-BOX SUBSTITUTION (7 points)
# ============================================================
#Given a 48-bit input, apply the eight S-boxes to produce a 32-bit output.
def sbox_substitution(bits48):
    #INSERT YOUR CODE HERE
    sbox_output = ""
    i = 0
    for table in SBOXES:
        block = bits48[i*6:(i+1)*6]
        
        sbox_row = f"{block[0:1]}{block[5:]}"
        sbox_row = int(sbox_row,2)

        sbox_col = f"{block[1:5]}"
        sbox_col = int(sbox_col,2)
        
        sbox_index = table[sbox_row][sbox_col]
        bin_value = bin(sbox_index)[2:]

        while len(bin_value) < 4:
            bin_value = f"0{bin_value}"
        sbox_output = f"{sbox_output}{bin_value}"

        # if i == 0:        TEST FOR WORKSHEET!!!
            # print(f"S1 Stats    Row: {sbox_row}    Column: {sbox_col}  Output: {sbox_output}")
        i = i+1

    

    return sbox_output  # Replace None with the 32-bit result.

# Question 4: Find row/column/output for 011011 in S1 (worksheet).
# Question 5: Run the supplied S-box test.
print('Question 5:')
print('S-box output =', sbox_substitution('000000' * 8))
# Question 6: Run the more complex 48-bit S-box test.
print('Question 6:')
print('S-box output =', sbox_substitution('011011101101110010001111010101100110001011111000'))


# ============================================================
# PART 3: FEISTEL FUNCTION & DES ENCRYPTION (8 points)
# ============================================================
def feistel(right32, round_key48):
    #INSERT YOUR CODE HERE
    E_right48 = permute(right32,E)
    xor48 = xor_bits(E_right48,round_key48)
    S_right32 = sbox_substitution(xor48)
    P_right32 = permute(S_right32,P)
    return P_right32  # Replace None with the 32-bit binary string.


# The following key schedule and encryption skeleton are PROVIDED.
# Do not modify them!!! Your three functions above complete the algorithm.
def rotate_left(bits, steps):
    return bits[steps:] + bits[:steps]

def des_round_keys(key64):
    key56 = permute(key64, PC1)
    c, d = key56[:28], key56[28:]
    keys = []
    for shift in SHIFTS:
        c = rotate_left(c, shift)
        d = rotate_left(d, shift)
        keys.append(permute(c + d, PC2))
    return keys

def des_encrypt_block(plain64, key64):
    initial = permute(plain64, IP)
    left, right = initial[:32], initial[32:]
    for round_key in des_round_keys(key64):
        left, right = right, xor_bits(left, feistel(right, round_key))
    # DES swaps final halves before the inverse initial permutation.
    return permute(right + left, IP_INV)


# Question 7: Feistel test with R and K given in hexadecimal.
# The provided hex_to_bits helper converts them to binary inputs.
print('Question 7:')
first_round_f = feistel(hex_to_bits('F0AAF0AA', 32), hex_to_bits('1B02EFFC7072', 48))
print('Feistel output (hex) =', bits_to_hex(first_round_f) if first_round_f is not None else None)

# Question 8: Encrypt the supplied plaintext with the supplied DES key.
print('Question 8:')
plain = hex_to_bits('0123456789ABCDEF')
key = hex_to_bits('133457799BBCDFF1')
# Once Parts 1-3 are complete, uncomment the next two lines:
ciphertext = des_encrypt_block(plain, key)
print('Ciphertext (hex) =', bits_to_hex(ciphertext))
