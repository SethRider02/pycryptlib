# Contains various encoding schemes used in cryptography


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


def text_to_bits(text):
    """Encodes a string as UTF-8 and returns its bits as a list of 0s and 1s."""
    return [
        (byte >> shift) & 1
        for byte in text.encode("utf-8")
        for shift in range(7, -1, -1)
    ]


def bits_to_text(bits):
    """Converts a bit list whose length is a multiple of 8 back into text."""
    if len(bits) % 8 != 0:
        raise ValueError("The number of bits must be a multiple of 8.")

    byte_values = []
    for start in range(0, len(bits), 8):
        value = 0
        for bit in bits[start:start + 8]:
            value = (value << 1) | bit
        byte_values.append(value)

    return bytes(byte_values).decode("utf-8")


def ascii_to_bits(ascii_string):
    """Converts given ascii text into a string of bits. Returns full string of bits with no delimeter."""
    ascii_bytes = ' '.join(format(ord(c),'08b') for c in ascii_string)
    ascii_bytes = ascii_bytes.replace(' ','')
    return ascii_bytes


def bits_to_ascii(bits):
    """Converts a string of bits into an ASCII string. Returns ASCII string if successful, or None if unsuccessful."""
    if len(bits) % 8 != 0:
        return None

    ascii_string = ''
    byte_size = int(len(bits)/8)
    ascii_list = []
    for i in range(0,byte_size):
        ascii_bin = bits[i*8:(i+1)*8]
        ascii_list.append(int(ascii_bin,2))

    for code in ascii_list:
        ascii_string = f'{ascii_string}{format(code,'c')}'

    return ascii_string


def hex_to_bits(hex_string, width=64):
    """Given hexadecimal text, return exactly width binary characters."""
    return format(int(hex_string, 16), f"0{width}b")


def bits_to_hex(bits):
    """Given binary text, return uppercase hexadecimal text (with leading zeros)."""
    return format(int(bits, 2), f"0{len(bits) // 4}X")