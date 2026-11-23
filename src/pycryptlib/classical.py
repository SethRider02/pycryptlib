from .encoding import digitize, undigitize
from .numtheory import mod_inverse
import math

#==================================#
#      SHIFT CIPHER FUNCTIONS      #
#==================================#

def shift_encrypt(plaintext, key):
    """Encrypts plaintext using a shift key from 0 to 25. Returns the ciphertext."""
    cnumbs = []
    for n in digitize(plaintext):
        cnumbs.append((n+key)%26)
    return undigitize(cnumbs)


def shift_decrypt(ciphertext, key):
    """Decrypts ciphertext when the shift key is known. Returns the plaintext."""
    pnumbs = []
    for n in digitize(ciphertext):
        pnumbs.append((n-key)%26)
    return undigitize(pnumbs)


def brute_force_shift(ciphertext):
    """Returns all 26 possible keys and corresponding plaintext outputs."""
    bruteval = ""
    for maykey in range(0,26):
        pnumbs = shift_decrypt(ciphertext,maykey)
        bruteval = bruteval+f"{pnumbs} Key = {maykey}\n"
    return bruteval

#==================================#
#     AFFINE CIPHER FUNCTIONS      #
#==================================#

def affine_encrypt(plaintext, a, b):
    """Encrypts plaintext with affine key (a, b). Returns ciphertext upon success."""
    if math.gcd(a,26) != 1:
        return None

    dctext = []
    for numb in digitize(plaintext):
        dctext.append((a*numb + b)%26)

    return undigitize(dctext)


def affine_decrypt(ciphertext, a, b):
    """Decrypts ciphertext with a known affine key (a, b). Returns plaintext upon success."""
    if math.gcd(a,b) != 1:
        return None

    dptext = []
    a_inv = mod_inverse(a,26)

    if a_inv == None:
        return None

    for numb in digitize(ciphertext):
        dptext.append(a_inv * (numb-b) % 26)

    return undigitize(dptext)


def brute_force_affine(ciphertext):
    """
    Returns every valid affine key and its candidate plaintext.
    Valid a values are exactly those for which gcd(a, 26) == 1.
    """
    bruteval = ''
    for a in range(26):
        for b in range(26):
            plaintext = affine_decrypt(ciphertext,a,b)
            if plaintext != None:
                bruteval = bruteval + f'{plaintext} Key = ({a},{b})\n'
    return bruteval


#==================================#
#    VIGENERE CIPHER FUNCTIONS     #
#==================================#

def vigenere_encrypt(plaintext, key):
    """Encrypts plaintext using a Vigenere key. Returns the ciphertext."""
    dkey = digitize(key)
    dctext = []
    i = 0

    for number in digitize(plaintext):
        dctext.append((number+dkey[i%len(key)])%26)
        i = i+1

    return undigitize(dctext)


def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext when the Vigenere key is known. Return plaintext."""    
    dkey = digitize(key)
    dptext = []
    i = 0

    for number in digitize(ciphertext):
        dptext.append((number-dkey[i%len(key)])%26)
        i = i+1

    return undigitize(dptext)


def brute_force_vigenere(ciphertext, known_word):
    """
    Tries every three-letter key and print candidates containing known_word.
    Return both the key and candidate plaintext when a match is found.
    WARNING: Only works with 3 letter Vigenere keys!
    """
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

    return key, pptext