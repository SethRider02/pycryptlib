# Contains functions required for DES (Data Encryption Standard)
import tables as T



def xor_bits(left, right):
    """Provided helper: bitwise XOR of two equal-length binary strings."""
    return ''.join('1' if a != b else '0' for a, b in zip(left, right))


def permute(bits, table):
    """Return bits reordered using the given permutation table. Use [T.] before your table
    to correctly grab from the tables file."""
    permutation = ""
    for index in table:
        permutation = f"{permutation}{bits[index-1:index]}"
    return permutation


def sbox_substitution(bits48):
    """Takes a 48 bit string and passes them through all S Boxes. Returns 32 bit string."""
    sbox_output = ""
    i = 0
    for table in T.SBOXES:
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

        i = i+1

    return sbox_output


def feistel(right32, round_key48):
    """Takes the right 32 bits and specified round key through a feistal round. Returns the right
    32 bits after primitive permutation (P) function."""
    E_right48 = permute(right32,T.E)
    xor48 = xor_bits(E_right48,round_key48)
    S_right32 = sbox_substitution(xor48)
    P_right32 = permute(S_right32,T.P)
    return P_right32


def rotate_left(bits, steps):
    """Shifts bits left by X amount of steps. Shift loops (ie. 1st bit becomes 32nd bit).
    Returns result of shifting."""
    return bits[steps:] + bits[:steps]


def des_round_keys(key64):
    """Generate round keys given the original 64-bit key. Returns list of keys."""
    key56 = permute(key64, T.PC1)
    c, d = key56[:28], key56[28:]
    keys = []
    for shift in T.SHIFTS:
        c = rotate_left(c, shift)
        d = rotate_left(d, shift)
        keys.append(permute(c + d, T.PC2))
    return keys


def des_encrypt_block(plain64, key64):
    """Takes a 64-bit block and encrypts with a 64-bit key. Returns cipher of 64-bits."""
    initial = permute(plain64, T.IP)
    left, right = initial[:32], initial[32:]
    for round_key in des_round_keys(key64):
        left, right = right, xor_bits(left, feistel(right, round_key))
    # DES swaps final halves before the inverse initial permutation.
    return permute(right + left, T.IP_INV)


def des_decrypt_block(cipher64,key64):
    """Decrypts a 64-bit cipher block with a given key. Returns 64-bit plaintext."""
    cipher64 = permute(cipher64,T.IP)
    left, right = cipher64[:32], cipher64[32:]
    reverse_keys = des_round_keys(key64)
    for i in range(0,16):
        # print('Using Key: ',(-1-i)%16)
        round_key = reverse_keys[-1-i]
        left, right = right, xor_bits(left, feistel(right, round_key))
    return permute(right+left,T.IP_INV)