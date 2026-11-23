# Contains various functions pertaining to number theory.
import math


def xor_bits(bitstring_1,bitstring_2):
    """XORs two strings of bits. Returns result as string."""
    result = ""
    if len(bitstring_1) != len(bitstring_2):
        return -1
    else:
        for i in range(0,len(bitstring_1)):
            if bitstring_1[i:i+1] == bitstring_2[i:i+1]:
                result = f"{result}0"
            else:
                result = f"{result}1"
        return result

def mod_inverse(a, n):
    """Finds mod inverse of a mod(n). Returns inverse if found or none if not found."""
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


def bin_exp(exponent):
    """Calculates the binary expansion of a given exponent. Returns a list of the power of 2's for the exponent."""
    twopower = []
    while(exponent != 0):
        i = 0
        while(exponent >= (2**i)):
            i=i+1
        i=i-1
        twopower.append(2**i)
        exponent = exponent - (2**i)

    return twopower


def fast_mod_exp(base, exponent, modulus):
    """Calculates a value given a base, positive exponent, and a modulus. Returns the value in the respective modulus."""
    if modulus <= 0:
        raise ValueError("modulus must be a positive integer.")
    if exponent < 0:
        raise ValueError("exponent must be nonnegative.")
    
    powers = bin_exp(exponent)
    result = 1
    current_power = 1
    current_value = base % modulus

    while current_power <= exponent:
        if current_power in powers:
            result = (result * current_value) % modulus
        current_value = (current_value * current_value) % modulus
        current_power = current_power * 2

    return result % modulus


def euler_totient(n):
    """Returns factors from 1 to n that are relatively prime to n."""
    factors = []
    for a in range(1,n):
        gcd = math.gcd(a,n)
        if gcd == 1:
            factors.append(a)
        else:
            continue

    phi = len(factors)
    return phi


