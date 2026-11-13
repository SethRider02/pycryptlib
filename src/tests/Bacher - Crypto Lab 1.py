"""
Crypto Lab 1: Classical Ciphers and GCD

Complete the functions below. Do not delete or alter the function names.
Submit your completed .py file to Canvas.
"""

# -----------------------------------------------------------------------------
# Provided alphabet mappings
# A -> 0, B -> 1, ..., Z -> 25
# -----------------------------------------------------------------------------

letter_dict = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
    'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
    'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17,
    'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22,
    'X': 23, 'Y': 24, 'Z': 25
}

number_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
    6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
    23: 'X', 24: 'Y', 25: 'Z'
}

# -----------------------------------------------------------------------------
# Part 1: Digitizing text
# -----------------------------------------------------------------------------

def digitize(text):
    """
    Convert text to a list of integers using A=0, ..., Z=25.
    For simplicity, you can assume no spaces or punctuation will be entered.
    Example: 'CAT' -> [2, 0, 19]
    """
    #INSERT YOUR CODE HERE
    numlist = []
    for t in text:
        for key, value in letter_dict.items():
            if t == key:
                numlist.append(value)
    return numlist


def undigitize(numbers):
    """
    Convert a list of integers between 0-25 back to a string of uppercase letters.
    Example: [2, 0, 19] -> 'CAT'
    """
    #INSERT YOUR CODE HERE
    word = ""
    for n in numbers:
        for key, value in number_dict.items():
            if n == key:
                word = f"{word}{value}"
    final = (f"{word.upper()}")
    return final



# -----------------------------------------------------------------------------
# Part 2: Shift cipher
# Encryption rule: E(x) = (x + k) mod 26
# Decryption rule: D(y) = (y - k) mod 26
# -----------------------------------------------------------------------------

def shift_encrypt(plaintext, key):
    """Encrypt plaintext using a shift key from 0 to 25. Return the ciphertext.
    HINT: Use your digitize(), modular arithmetic, and undigitize() functions. """
    #INSERT YOUR CODE HERE
    pnumbs = digitize(plaintext)
    cnumbs = []
    for n in pnumbs:
        cnumbs.append((n+key)%26)
    ctext = undigitize(cnumbs)
    return ctext


def shift_decrypt(ciphertext, key):
    """Decrypt ciphertext when the shift key is known. Return the plaintext."""
    #INSERT YOUR CODE HERE
    cnumbs = digitize(ciphertext)
    pnumbs = []
    for n in cnumbs:
        pnumbs.append((n-key)%26)
    dtext = undigitize(pnumbs)
    return dtext


def brute_force_shift(ciphertext):
    """Print all 26 possible keys and corresponding plaintext outputs."""
    #INSERT YOUR CODE HERE
    bruteval = ""
    for maykey in range(0,26):
        pnumbs = shift_decrypt(ciphertext,maykey)
        bruteval = bruteval+f"{pnumbs} Key = {maykey}\n"
    return bruteval



# -----------------------------------------------------------------------------
# Part 3: Greatest common divisor
# -----------------------------------------------------------------------------

def gcd(a, b):
    """Compute gcd(a, b) using the Euclidean Algorithm. Return the GCD (an integer).
    HINT: repeatedly replace (a, b) with (b, a % b) until b == 0."""
    #INSERT YOUR CODE HERE
    while b != 0:
        a,b = b,a%b

    return a



# -----------------------------------------------------------------------------
# Part 4/5: Affine cipher
# Encryption rule: E(x) = (a*x + b) mod 26
# Decryption rule: D(y) = a^(-1) * (y - b) mod 26
# A valid 'a' must satisfy gcd(a, 26) = 1.

# -----------------------------------------------------------------------------
# Provided helper function for the affine cipher.
# Finds a^(-1) mod m by checking possible values.
def mod_inverse(a, m=26):
    for candidate in range(m):
        if (a * candidate) % m == 1:
            return candidate
    return None #Return None if no inverse 
# -----------------------------------------------------------------------------

def affine_encrypt(plaintext, a, b):
    """Encrypt plaintext with affine key (a, b)."""
    #INSERT YOUR CODE HERE
    if gcd(a,26) != 1:
        return None

    dptext = digitize(plaintext)
    dctext = []

    for numb in dptext:
        dctext.append((a*numb + b)%26)

    ciphertext = undigitize(dctext)

    # 1. Reject invalid a values where gcd(a, 26) != 1.
    # 2. Digitize the plaintext.
    # 3. Apply (a*x + b) % 26 to each value.
    # 4. Convert back to letters.

    return ciphertext


def affine_decrypt(ciphertext, a, b):
    """Decrypt ciphertext with a known affine key (a, b)."""
    #INSERT YOUR CODE HERE
    if gcd(a,b) != 1:
        return None

    dctext = digitize(ciphertext)
    dptext = []
    a_inv = mod_inverse(a,26)

    if a_inv == None:
        return None

    for numb in dctext:
        dptext.append(a_inv * (numb-b) % 26)

    plaintext = undigitize(dptext)
    
    # 1. Reject invalid a values where gcd(a, 26) != 1.
    # 2. Find a_inv = mod_inverse(a, 26). HINT: Use the mod_inverse() function given above.
    # 3. Apply a_inv * (y - b) % 26 to each value.
    # 4. Convert back to letters.
    return plaintext


def brute_force_affine(ciphertext):
    """
    Print every valid affine key and its candidate plaintext.
    Valid a values are exactly those for which gcd(a, 26) == 1.
    Try a = 0..25 and b = 0..25. Remember you can skip invalid a values.
    """
    #INSERT YOUR CODE HERE
    bruteval = ''
    for a in range(26):
        for b in range(26):
            plaintext = affine_decrypt(ciphertext,a,b)
            if plaintext != None:
                bruteval = bruteval + f'{plaintext} Key = ({a},{b})\n'
    return bruteval


# -----------------------------------------------------------------------------
# TEST / LAB AREA
# Use the below to test your functions and answer the worksheet questions.
# -----------------------------------------------------------------------------
"""
print("PART 1: DIGITIZING TEXT")
print("1. digitize('COAST GUARD') is:", digitize("COASTGUARD"))
print("2. undigitize(digitize(CRYPTO)) is:", undigitize(digitize("CRYPTO")))

print("PART 2: SHIFT CIPHER")
print("3. shift_decrypt(TLLATLHAAOLSPIYHYF): ", shift_decrypt("TLLATLHAAOLSPIYHYF", 7))
"""
print("4. Decrypted VKRIMHZKTIARBLYNG:")
print(brute_force_shift("VKRIMHZKTIARBLYNG"))
"""

print("PART 3: GCD")
print("gcd(48, 18) should be 6:", gcd(48, 18))
print("gcd(35, 26) should be 1:", gcd(35, 26))

print("PART 4: AFFINE CIPHER")
print("6. Decrypt QCCZIZVAAV with a=5, b=8:", affine_decrypt("QCCZIZVAAV", 5, 8))
print("7. My encrypted name is:", affine_encrypt("SETH", 17, 5))
print("7. My decrypted name is:", affine_decrypt("ZVQU", 17, 5))

print("PART 5: CIPHER CRACKING")
print("8. Decrypt CYHSXUFWZUFAYHOMYWUXKTYHK:")
print(brute_force_affine("CYHSXUFWZUFAYHOMYWUXKTYHK"))

print(brute_force_affine(affine_encrypt("AAAA",17,5)))
"""