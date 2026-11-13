# Contains functions for both KidRSA and RSA
from .encoding import digitize, undigitize
from .numtheory import mod_inverse

def kidrsa_keygen(a, b, a0, b0):
    """Takes given KidRSA components to compute M, e, d, and n. Returns tuple of values in the same order."""
    if a * b <= 1:
        raise ValueError("a*b must be greater than 1.")

    M = a*b - 1
    e = a0*M + a
    d = b0*M + b
    n = (e*d-1)/M

    return (M, e, d, n)


def kidrsa_encrypt(message, e, n):
    """Encrypts a string message given e and n. Returns ciphertext as a list of encoded values."""
    dmess = digitize(message)
    cmess = []
    for num in dmess:
        newnum = (e*num)%n
        cmess.append(newnum)

    return cmess


def kidrsa_decrypt(ciphertext, d, n):
    """Decrypts a list of encoded integers using d and n. Returns plaintext as a string."""
    pmess = []
    for num in ciphertext:
        newnum = (num*d)%n
        pmess.append(newnum)

    return undigitize(pmess)


def rsa_keygen(p, q, e):
    """Generates RSA key values given p, q, and e. Returns a tuple with n, e, and d."""
    n = p*q
    phi_n = (p-1)*(q-1)
    d = mod_inverse(e,phi_n)
    return (n,e,d)


def rsa_encrypt(plaintext,p,q,e):
    """Encrypts plaintext list of integers using RSA. Returns ciphertext as list of integers."""
    keys = rsa_keygen(p,q,e)
    n = keys[0]
    e = keys[1]
    ciphertext = []

    for i in range(0,len(plaintext)):
        m = plaintext[i]
        c = pow(m,e,n)
        ciphertext.append(c)

    return ciphertext


def rsa_decrypt(ciphertext,p,q,e):
    """Decrypts ciphertext list of integers using RSA. Returns plaintext as list of integers."""
    keys = rsa_keygen(p,q,e)
    n = keys[0]
    d = keys[2]
    recovered_plaintext = []

    for i in range(0,len(ciphertext)):
        c = ciphertext[i]
        m = pow(c,d,n)
        recovered_plaintext.append(m)