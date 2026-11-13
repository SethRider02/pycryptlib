"""
Programming Assignment 6: Euler's Totient, Modular Inverses & Textbook RSA
50 minutes | 20 points

Name: Seth Bacher

Complete the functions and exercises below. Record your answers to
Questions 1-8 on the worksheet. Do not change the provided function names.
"""
#Need to import math for gcd function
import math

# ============================================================
# PART 1: EULER'S TOTIENT FUNCTION (6 points)
# ============================================================

#Function to return the number of integers from 1 to n that are relatively prime to n.
def euler_totient(n):
    factors = []
    for a in range(1,n):
        gcd = math.gcd(a,n)
        if gcd == 1:
            factors.append(a)
        else:
            continue

    phi = len(factors)
    return phi #Replace 'None' with the correct function output.


# Question 1: Calculate phi(15), phi(29), and phi(100).
print("Question 1:")
print("phi(29) =", euler_totient(29))
print("phi(12345) =", euler_totient(12345))
print("phi(8675309) =", euler_totient(8675309))

# Question 2: Why is phi(p) = p - 1 for prime p?
# Answer this question on your worksheet.

# Question 3: What is the formula for phi(pq) for distinct primes p, q?
# Answer this question on your worksheet.


# ============================================================
# PART 2: MODULAR INVERSES (7 points)
# ============================================================

#Function to return the modular inverse of a modulo n, or 'None' if no inverse exists.
def mod_inverse(a, n):
    gcd = math.gcd(a,n)
    if gcd == 1:
        for x in range(1,n):
            inverse = (a*x)%n
            if inverse == 1:
                break
            else:
                continue
    else:
        return None
    return x

# Question 4: Find two modular inverses.
print("Question 4:")
print("Inverse of 17 mod 43 =", mod_inverse(17, 43))
print("Inverse of 7 mod 100003 =", mod_inverse(7, 100003))

# Question 5: Find mod_inverse(437, 10879) and explain the result.
print("Question 5:")
print("Inverse of 437 mod 10879 =", mod_inverse(437, 10879))
# Explain the result on your worksheet.

# Question 6: Explain the theorem we can use for modular inverses when the modulus is prime. 
# Answer on your worksheet.


# ============================================================
# PART 3: TEXTBOOK RSA (7 points)
# ============================================================

#Return the RSA key parameters as (n, e, d).
def rsa_keygen(p, q, e):
    n = p*q
    phi_n = (p-1)*(q-1)
    d = mod_inverse(e,phi_n)
    return (n,e,d) #Replace 'None' with the correct function output.


# Question 7: Generate RSA keys using p=211, q=223, e=17.
print("Question 7:")
keys = rsa_keygen(211, 223, 17)
print("RSA keys (n, e, d) =", keys)

# Question 8: Encrypt and decrypt the integer list below.
# Use Python's pow(base, exponent, modulus) and the keys from Q7.
plaintext = [2, 7, 12, 18, 25]
ciphertext = []
recovered_plaintext = []
n = keys[0]
e = keys[1]
d = keys[2]

for i in range(0,len(plaintext)):
    m = plaintext[i]
    c = pow(m,e,n)
    ciphertext.append(c)

for i in range(0,len(ciphertext)):
    c = ciphertext[i]
    m = pow(c,d,n)
    recovered_plaintext.append(m)


print("Question 8:")
print("Plaintext List:", plaintext)
print("Ciphertext List:", ciphertext)
print("Recovered Plaintext List:", recovered_plaintext)
