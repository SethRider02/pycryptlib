from .encoding import text_to_bits, bits_to_text
import secrets


def xor_bits(data_bits, keystream_bits):
    """Take two streams of bits and xors them. Returns the resulting stream of bits."""
    if len(data_bits) != len(keystream_bits):
        raise ValueError("Data and keystream must have the same length.")
    if not all(bit in (0, 1) for bit in data_bits + keystream_bits):
        raise ValueError("Data and keystream must contain only 0s and 1s.")

    i = 0
    cipherbits = []
    while i < len(data_bits):
        if data_bits[i] != keystream_bits[i]:
            cipherbits.append(1)
        else:
            cipherbits.append(0)
        i = i+1

    return cipherbits


def generate_one_time_pad(length):
    """Generates a one time pad of a specified length using Python's secret module."""
    if length < 0:
        raise ValueError("Length cannot be negative.")

    i = 0
    rand_pad = []
    while i < length:
        rand_pad.append(secrets.randbits(1))
        i = i+1

    return rand_pad


def otp_encrypt(plaintext):
    """Encrypts the plaintext using an OTP"""
    bit_text = text_to_bits(plaintext)
    ot_pad = generate_one_time_pad(len(bit_text))
    cbit_text = xor_bits(bit_text, ot_pad)
    return (cbit_text,ot_pad)


def otp_decrypt(ciphertext_bits, otp):
    """XORs the ciphertext bit list with the one-time pad (keystream) used to encrypt the ciphertext, and converts the resulting bit list back to an ASCII plaintext string.
    """
    pbit_text = xor_bits(ciphertext_bits,otp)
    return bits_to_text(pbit_text)