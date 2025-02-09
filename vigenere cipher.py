import itertools

# Vigenère Table
VT = [[chr(((i + j) % 26) + 65) for j in range(26)] for i in range(26)]

# XOR Obfuscation
def signature(text):
    return ''.join(chr(ord(c) ^ 42) for c in text)

def create_dfbh_iv_matrix(key):
    key = "".join(dict.fromkeys(key.upper().replace("J", "I"))) 
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key += "".join([c for c in alphabet if c not in key])
    
    matrix = [list(key[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def encrypt_dfbh_iv(text, matrix):
    text = ''.join(filter(str.isalpha, text.upper())).replace("J", "I")
    pairs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] != text[i + 1]:
            pairs.append(text[i] + text[i + 1])
            i += 2
        else:
            pairs.append(text[i] + "X")
            i += 1
    cipher_text = ""
    for pair in pairs:
        pos1 = find_position(matrix, pair[0])
        pos2 = find_position(matrix, pair[1])
        if pos1 is None or pos2 is None:
            print(f"Error: Character '{pair[0]}' or '{pair[1]}' not found in matrix.")
            exit()
        row1, col1 = pos1
        row2, col2 = pos2
        if row1 == row2:  
            cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  
            cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    return cipher_text

dfbh_iv_key = "aquztt"
dfbh_iv_matrix = create_dfbh_iv_matrix(dfbh_iv_key)
made_by = "Made By:"
author = "Er.Jatin Joshi"
clean_author = ''.join(filter(str.isalpha, author.upper())).replace("J", "I")  
EA = encrypt_dfbh_iv(clean_author, dfbh_iv_matrix)
print(made_by, author)
if EA != "FPGUULOHMWIK":  
    print("Unauthorized author! Exiting...")
    exit()

# Function to Convert Text to Numbers
def text_to_numbers(text):
    return [ord(c) - ord('A') for c in text if 'A' <= c <= 'Z']

# Get User Input
PT = input("Enter Plain Text: ").upper().replace(" ", "")
K = input("Enter Key: ").upper().replace(" ", "")

# Validation
if not PT or not K or not any(c.isalpha() for c in PT) or not any(c.isalpha() for c in K):
    print("Error: Plain Text and Key must contain at least one alphabetical character!")
    exit()

# Check if key and plaintext are of the same length
if len(PT) != len(K):
    print(f"Error: The key must be of the same length as the plain text ({len(PT)} characters).")
    exit()

PT_numbers = text_to_numbers(PT)
K_numbers = text_to_numbers(K)

# Encrypt using Vigenère Cipher
CT = ''.join(VT[p][k] for p, k in zip(PT_numbers, K_numbers))

print("Cipher Text is:", CT)
