"""
Programming Assignment 5: Kid RSA and Fast Modular Exponentiation
50 minutes | 25 points

Name: 2/c Seth Bacher

Complete the student functions in Parts 1, 2, and the binary expansion
function in Part 3. Note: The fast_mod_exp() function is PROVIDED. DO NOT EDIT IT!

Keep the function names and test areas. Use terminal output to complete
the corresponding numbered worksheet questions.
"""

# ============================================================
# PROVIDED HELPER FUNCTIONS (DO NOT EDIT!)
# ============================================================
def digitize(my_string):
    """Convert uppercase A-Z text into integers: A=0, ..., Z=25."""
    num_list = []
    for char in my_string:
        if not "A" <= char <= "Z":
            raise ValueError("Only uppercase letters A-Z are allowed.")
        num_list.append(ord(char) - ord("A"))
    return num_list

def undigitize(num_list):
    """Convert a list of integers from 0 to 25 into uppercase text."""
    my_string = ""
    for value in num_list:
        if not 0 <= value <= 25:
            raise ValueError("Each recovered letter value must be 0 through 25.")
        my_string += chr(int(value) + ord("A"))
    return my_string

# ============================================================
# PART 1 - KID RSA KEY GENERATION
# ============================================================
# Use the formulas on the worksheet to calculate M, e, d, and n.
def kidrsa_keygen(a, b, a0, b0):
    if a * b <= 1:
        raise ValueError("a*b must be greater than 1.")

    #Replace each 'None' with the correct expression.
    M = a*b - 1
    e = a0*M + a
    d = b0*M + b
    n = (e*d-1)/M

    return (M, e, d, n)


print("PART 1 - KID RSA KEY GENERATION")

# Worksheet Question 1
keys = kidrsa_keygen(137, 251, 43, 67)
print("1. Tuple (M, e, d, n):", keys)

# Worksheet Question 2
M, e, d, n = keys
if M !=None and e != None and d != None and n!=None:
    print("2. (e*d) % n:", (e * d) % n)
else:
    print("2. Complete the kidrsa_keygen function before answering Question 2!")

#Worksheet Question 3
print("3. (Complete on worksheet)")


# ============================================================
# PART 2 - KID RSA ENCRYPTION AND DECRYPTION
# ============================================================

#Complete the below function to encrypt a plaintext message using Kid RSA. 
# Hint: Use the digitize(my_string) helper function.
def kidrsa_encrypt(message, e, n):
    dmess = digitize(message)
    cmess = []
    for num in dmess:
        newnum = (e*num)%n
        cmess.append(newnum)

    return cmess #Replace 'None' with a list of integers representing the ciphertext.

#Complete the below function to decrypt a list of integers using Kid RSA. 
# Hint: Use the undigitize(num_list) helper function.
def kidrsa_decrypt(ciphertext, d, n):
    pmess = []
    for num in ciphertext:
        newnum = (num*d)%n
        pmess.append(newnum)

    return undigitize(pmess) #Replace 'None' with the plaintext string.


print("\nPART 2 - KID RSA ENCRYPTION AND DECRYPTION")

# Workshet Question 4
encrypted_text = kidrsa_encrypt("ACADEMY",e,n)
if encrypted_text is not None:
    print("4. Ciphertext list for ACADEMY:", encrypted_text)
else:
    print("4. Complete the kidrsa_encrypt function before answering Question 4!")

# Worksheet Question 5
ciphertext_to_decrypt = [2957470, 20702290, 0, 26617230, 28095965, 8872410, 29574700, 0, 25138495, 4436205]
recovered_plaintext = kidrsa_decrypt(ciphertext_to_decrypt, d, n)
if recovered_plaintext is not None:
    print("5. Recovered plaintext:", recovered_plaintext)
else:
    print("5. Complete the kidrsa_decrypt function before answering Question 5!")

#Worksheet Question 6
print("6. (Complete on worksheet)")

# ============================================================
# PART 3 - FAST MODULAR EXPONENTIATION
# ============================================================

#TO DO: Complete the below function to obtain the binary expansion of a given exponent.
def bin_exp(exponent):
    twopower = []
    while(exponent != 0):
        i = 0
        while(exponent >= (2**i)):
            i=i+1
        i=i-1
        twopower.append(2**i)
        exponent = exponent - (2**i)

    return twopower #Replace 'None' with the binary expansion as a list of powers of 2


# PROVIDED FAST MODULAR EXPONENTIATION FUNCTION (DO NOT EDIT!)
def fast_mod_exp(base, exponent, modulus):
    if modulus <= 0:
        raise ValueError("modulus must be a positive integer.")
    if exponent < 0:
        raise ValueError("exponent must be nonnegative.")
    #Step 1: Get the binary expansion of the exponent.
    powers = bin_exp(exponent)
    #Step 2: Initialize required variables.
    result = 1
    current_power = 1
    current_value = base % modulus
    #Step 3: Work through successive powers of 2.
    while current_power <= exponent:
        #Step 4: Check if we need the current power. If it appears in binary expansion, multiply its modular value into the result.
        if current_power in powers:
            result = (result * current_value) % modulus
        #Step 5: Square the current modular value. (Moves us from base^1 to base^2 to base^4 etc.)
        current_value = (current_value * current_value) % modulus
        #Step 6: Double the power for the next iteration.
        current_power = current_power * 2
    #Step 7: Return the final result.
    return result % modulus


print("\nPART 3 - FAST MODULAR EXPONENTIATION")

# Worksheet Question 7
if bin_exp(12345) is not None:
    print("7a. bin_exp(12345):", bin_exp(12345))
    print("7b. bin_exp(8675309):", bin_exp(8675309))
else:
    print("7. Complete the bin_exp function before answering Question 7!")

# Worksheet Question 8 (WARNING: Your bin_exp function must work first!)
if bin_exp(13) is not None:
    print("8a. 7^13 mod 33:", fast_mod_exp(7, 13, 33))
    print("8b. 161^81 mod 389:", fast_mod_exp(161, 81, 389))
    print("8c. 123^4567 mod 10007:", fast_mod_exp(123, 4567, 10007))
else:
    print("8. Complete the bin_exp function before answering Question 8!")