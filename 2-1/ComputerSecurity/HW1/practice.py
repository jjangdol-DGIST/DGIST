import random


def generate_key():
    """
    Generates a random string of length 17 over the alphabet [A..Z].
    """
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=17))


def encrypt_vigenere_enhanced(plaintext):
    """
    Encrypts plaintext using the enhanced Vigenere cipher.
    """
    # Generate random string and prepend it to plaintext
    key = generate_key()
    x = key + plaintext.upper()

    # Compute ciphertext using enhanced Vigenere algorithm
    y = [ord(x[i]) - 65 for i in range(17)]
    for i in range(17, len(x)):
        yi = (y[i-17] + ord(x[i]) - 65) % 26
        y.append(yi)
    key_length = len(key)
    while key_length < len(y):
        key += key
        key_length = len(key)
    ciphertext = ""
    for i in range(len(y)):
        shift = ord(key[i]) - 65
        ciphertext += chr((y[i] + shift) % 26 + 65)
    return ciphertext


def decrypt_vigenere_enhanced(ciphertext):
    """
    Decrypts ciphertext encrypted with the enhanced Vigenere cipher.
    """
    # Generate random string from ciphertext
    key_length = len(ciphertext) % 17
    key = ciphertext[:key_length]

    # Compute y from ciphertext using Vigenere algorithm
    y = [ord(c) - 65 for c in ciphertext[key_length:]]
    for i in range(len(y)):
        shift = ord(key[i % len(key)]) - 65
        y[i] = (y[i] - shift) % 26

    # Convert y to plaintext
    plaintext = ""
    for i in range(17, len(y)):
        xi = (y[i] - y[i-17]) % 26
        plaintext += chr(xi + 65)
    return plaintext.lower()



plaintext = "Hello World"
ciphertext = encrypt_vigenere_enhanced(plaintext)
print("Encrypted message:", ciphertext)

decrypted_text = decrypt_vigenere_enhanced(ciphertext)
print("Decrypted message:", decrypted_text)
