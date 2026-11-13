"""
Crypto Lab 2: Vigenere Cipher

Complete the functions below. Do not delete or alter the function names.
Submit your completed .py file to Canvas.

For simplicity, assume all inputs contain uppercase letters only with no spaces
or punctuation unless otherwise noted.
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
# Provided helper functions (DO NOT TOUCH)
# -----------------------------------------------------------------------------

def digitize(text):
    """Convert uppercase letters to numbers using A=0, ..., Z=25."""
    return [letter_dict[letter] for letter in text]


def undigitize(numbers):
    """Convert list of numbers from 0-25 back to uppercase letters."""
    return ''.join(number_dict[number] for number in numbers)

# -----------------------------------------------------------------------------
# Part 1: Vigenere encryption
# Encryption rule: C_i = (P_i + K_i) mod 26
# The key repeats as needed across the plaintext.
# -----------------------------------------------------------------------------

def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using a Vigenere key. Return the ciphertext."""
    # INSERT YOUR CODE HERE
    dptext = digitize(plaintext)
    dkey = digitize(key)
    dctext = []
    i = 0

    for number in dptext:
        dctext.append((number+dkey[i%len(key)])%26)
        i = i+1

    ctext = undigitize(dctext)

    # HINTS:
    # 1. Convert plaintext and key to numbers with digitize().
    # 2. Use i % len(key) to repeat the key across the message.
    # 3. Apply (plaintext_number + key_number) % 26.
    # 4. Convert the result back to letters with undigitize().
    return ctext


# -----------------------------------------------------------------------------
# Part 2: Vigenere decryption
# Decryption rule: P_i = (C_i - K_i) mod 26
# -----------------------------------------------------------------------------

def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext when the Vigenere key is known. Return plaintext."""
    # INSERT YOUR CODE HERE
    
    dctext = digitize(ciphertext)
    dkey = digitize(key)
    dptext = []
    i = 0

    for number in dctext:
        dptext.append((number-dkey[i%len(key)])%26)
        i = i+1

    ptext = undigitize(dptext)

    # HINT: This should look very similar to vigenere_encrypt().
    return ptext


# -----------------------------------------------------------------------------
# Part 3: Constrained brute force
# We know the unknown key has EXACTLY 3 uppercase letters.
# A helper below generates all 26^3 possible keys.
# -----------------------------------------------------------------------------

def brute_force_vigenere(ciphertext, known_word):
    """
    Try every three-letter key and print candidates containing known_word.
    Return both the key and candidate plaintext when a match is found.
    """
    # INSERT YOUR CODE HERE
    # HINTS:
    pptext = ''
    pkey = [0,0,0]
    key = ''

    while pkey[0] != 26:

        if known_word in pptext:
            break
        
        key = undigitize(pkey)
        pptext = vigenere_decrypt(ciphertext,key)
        if pkey[2] == 25:
            pkey[1]+=1
            pkey[2] = 0
        else:
            pkey[2]+=1

        if pkey[1] == 25:
            pkey[0]+=1
            pkey[1] = 0

    # 1. Loop through all possible keys of length 3
    # 2. Decrypt the ciphertext using each possible key.
    # 3. Use in operator to search for known_word in the decrypted, candidate plaintext.
    # 4. Return the key and plaintext only when the known word appears.
    return key, pptext


# -----------------------------------------------------------------------------
# TEST AREA
# Uncomment these lines as you complete each part.
# -----------------------------------------------------------------------------

print("PART 1: VIGENERE ENCRYPTION")
print("1. Encrypt COAST GUARD ACADEMY with key CRYPTOGRAPHY:", vigenere_encrypt("COASTGUARDACADEMY", "CRYPTOGRAPHY"))

print("PART 2: VIGENERE DECRYPTION")
print("2. Decrypt ZEZBSETBMRNTJVNAET with key NAVIGATION:", vigenere_decrypt("ZEZBSETBMRNTJVNAET", "NAVIGATION"))

print("PART 3: CONSTRAINED BRUTE FORCE")
print(brute_force_vigenere("VNIUCAUKNEXYRZEFASKTGCBIIKNGXEEOPJKR", "CIPHER"))