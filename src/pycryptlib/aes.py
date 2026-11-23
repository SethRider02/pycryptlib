# Contains functions used for Advanced Encryption Scheme (AES)
import aes_tables as aest
import encoding as en

# Uncomment for testing
"""P_hex = "50415353574F52444953534543555245"
K_hex = "4B4559534152455241444943414C594F"

FIPS_P = "3243F6A8885A308D313198A2E0370734"
FIPS_K = "2B7E151628AED2A6ABF7158809CF4F3C"
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

rcon = [1,2,4,8,16,32,64,128,27,54]

mcmatrix = [2,1,1,3,3,2,1,1,1,3,2,1,1,1,3,2]
inverse_mcmatrix = [14,9,13,11,11,14,9,13,13,11,14,9,9,13,11,14]


def matrix_print(state):
    """Prints matrix as viewed in AES, primarily for testing. Prints state, no return value."""
    print(f'''{state[0]} {state[4]} {state[8]} {state[12]}
{state[1]} {state[5]} {state[9]} {state[13]}
{state[2]} {state[6]} {state[10]} {state[14]}
{state[3]} {state[7]} {state[11]} {state[15]}''')

def multiply_by_02(a):
    """Multiply byte a by 02 in AES GF(2^8)."""
    return ((a << 1) ^ (27 if a & 128 else 0)) & 255

def multiply_by_03(a):
    """Multiply byte a by 03 in AES GF(2^8)."""
    return multiply_by_02(a) ^ a

def multiply_by_09(a):
    """Multiply byte a by 09 in AES GF(2^8)."""
    a2 = multiply_by_02(a)
    a4 = multiply_by_02(a2)
    a8 = multiply_by_02(a4)
    return a8 ^ a

def multiply_by_11(a):
    """Multiply byte a by 11 in AES GF(2^8)."""
    a2 = multiply_by_02(a)
    a4 = multiply_by_02(a2)
    a8 = multiply_by_02(a4)
    return a8 ^ a2 ^ a

def multiply_by_13(a):
    """Multiply byte a by 13 in AES GF(2^8)."""
    a2 = multiply_by_02(a)
    a4 = multiply_by_02(a2)
    a8 = multiply_by_02(a4)
    return a8 ^ a4 ^ a

def multiply_by_14(a):
    """Multiply byte a by 14 in AES GF(2^8)."""
    a2 = multiply_by_02(a)
    a4 = multiply_by_02(a2)
    a8 = multiply_by_02(a4)
    return a8 ^ a4 ^ a2
    
mult = {1:lambda a:a, 2: multiply_by_02, 3: multiply_by_03, 9: multiply_by_09,
        11: multiply_by_11, 13: multiply_by_13, 14: multiply_by_14}


def key_schedule(key):
    """Takes a key of 128 bits and creates the list of roundkeys. Returns list of round keys as ints."""
    words = [key[i:i+4] for i in range(0, 16, 4)]
    for i in range(4, 44):
        temp = words[i-1].copy()
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]                 # RotWord
            temp = [aest.sub_bytes[b] for b in temp]   # SubWord
            temp[0] ^= rcon[i//4 - 1]
        words.append([words[i-4][j] ^ temp[j] for j in range(4)])
    return [sum(words[4*r:4*r+4], []) for r in range(11)]


def ARK(state, round_key):
    """XORs the current state with a specific round key. Returns output state."""
    output_xor = []
    for i in range(0,16):
        output_xor.append(state[i]^round_key[i])

    return output_xor

def SB(state):
    """Takes current state and maps to sub bytes table. Returns output state."""
    output_sb = []
    for i in range(0,16):
        output_sb.append(aest.sub_bytes[state[i]])
    return output_sb

def SR(state):
    """Shifts rows of state according to AES encryption. Returns output state."""
    output_shift = []
    for i in range(0,16,4):
        output_shift.append(state[i])
        output_shift.append(state[(i+5)%16])
        output_shift.append(state[(i+10)%16])
        output_shift.append(state[(i+15)%16])
    return output_shift

def MC(state):
    """Mixes columns of state for AES encryption. Returns output state."""
    output_mixed = []
    for c in range(0,4):
        col = state[4*c:4*c + 4]
        for r in range(0,4):
            val = 0
            for k in range(0,4):
                val ^= mult[mcmatrix[4*k + r]](col[k])
            output_mixed.append(val)   
    return output_mixed

def AES_encrypt(plaintext,key):
    """Encrypts using AES-128 given a 16 byte hex string of plaintext and 16 byte key. Returns ciphertext as hex string."""
    ptext = en.hex_to_bytes(plaintext)
    init_key = en.hex_to_bytes(key)

    round_keys = key_schedule(init_key)
    state = ARK(ptext,round_keys[0])
    for round_number in range(1,10):
        state = SB(state)
        state = SR(state)
        state = MC(state)
        state = ARK(state,round_keys[round_number])
    # Final round without mix columns
    state = SB(state)
    state = SR(state)
    state = ARK(state,round_keys[10])
    return en.bytes_to_hex(state)


def SB_inverse(state):
    """Takes current state and maps to inverse sub byte table. Returns output state."""
    output_sb = []
    for i in range(0,16):
        output_sb.append(aest.inverse_sub_bytes[state[i]])
    return output_sb

def SR_inverse(state):
    """Shifts rows of state according to AES decryption. Returns output state."""
    output_shift = []
    for i in range(0,16,4):
        output_shift.append(state[i])
        output_shift.append((state[(i-3)%16]))
        output_shift.append((state[(i-6)%16]))
        output_shift.append((state[(i-9)%16]))
    return output_shift

def MC_inverse(state):
    """Mixes columns of state for AES decryption. Returns output state."""
    output_mixed = []
    for c in range(0,4):
        col = state[4*c:4*c + 4]
        for r in range(0,4):
            val = 0
            for k in range(0,4):
                val ^= mult[inverse_mcmatrix[4*k + r]](col[k])
            output_mixed.append(val) 
    return output_mixed

def AES_decrypt(ciphertext,key):
    """Decrypts using AES-128 given a ciphertext 16 byte hex string and 16 byte initial key. Returns plaintext as string."""
    ctext = en.hex_to_bytes(ciphertext)
    init_key = en.hex_to_bytes(key)

    round_keys = key_schedule(init_key)
    state = ARK(ctext,round_keys[10])
    for round_number in range(9,0,-1):
        state = SR_inverse(state)
        state = SB_inverse(state)
        state = ARK(state,round_keys[round_number])
        state = MC_inverse(state)
    state = SR_inverse(state)
    state = SB_inverse(state)
    state = ARK(state,round_keys[0])
    return en.bytes_to_hex(state)

"""print("Plaintext:",en.int_to_text(en.hex_to_bytes(P_hex)))
C_hex = AES_encrypt(P_hex,K_hex)
print("Ciphertext:",C_hex)
R_hex = AES_decrypt(C_hex,K_hex)
print("Recovered:",en.int_to_text(en.hex_to_bytes(R_hex)))"""