import random

from auxiliary import LATIN_ALP_LEN, read_file, write_file, preview_files


def generate_vigenere_matrix(toss_letters: bool, capital_letters: bool):
    alphabet = []
    first_letter = 'A' if capital_letters else 'a'
    first_letter_ascii = ord(first_letter)

    for pos in range(LATIN_ALP_LEN):
        alphabet.append(chr(first_letter_ascii + pos))

    if toss_letters:
        random.shuffle(alphabet)

    v_matrix = []


    print("Vigenere matrix")
    for i, letter in enumerate(alphabet):
        row = alphabet[i:] + alphabet[:i]
        v_matrix.append(row)
        print(row)

    return v_matrix

def encrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix):

    original_text = read_file(file_path)

    encrypted_list = []


    current_key_pos = -1
    key_len = len(key_str)
    for char in original_text:
        if char.isalpha():
            is_upper_char = char.isupper()
            char_index = ord(char) - ord('A' if is_upper_char else 'a')

            current_key_pos = (current_key_pos + 1) % key_len

            key_letter = key_str[current_key_pos]
            is_upper_key = key_letter.isupper()

            key_index = ord(key_letter) - ord('A' if is_upper_key else 'a')

            encrypted_list.append(v_matrix[key_index][char_index])
        else:
            encrypted_list.append(char)

    encrypted_text = ''.join(encrypted_list)
    return encrypted_text


def decrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix):
    original_text = read_file(file_path)

    encrypted_list = []

    current_key_pos = -1
    key_len = len(key_str)
    for char in original_text:
        if char.isalpha():
            current_key_pos = (current_key_pos + 1) % key_len
            key_letter = key_str[current_key_pos]
            is_upper_key = key_letter.isupper()

            key_index = ord(key_letter) - ord('A' if is_upper_key else 'a')

            is_upper_char = char.isupper()
            char_index = v_matrix[key_index].index(char.upper() if is_upper_char else char.lower())
            encrypted_list.append(v_matrix[0][char_index])

        else:
            encrypted_list.append(char)

    encrypted_text = ''.join(encrypted_list)
    return encrypted_text

if __name__ == "__main__":
    file_name = "test.txt"
    encV = f"encV_{file_name}"
    decV = f"decV_{file_name}"

    key = "hello"

    matrix = generate_vigenere_matrix(False, capital_letters=False)
    write_file(encV, encrypt_msg_by_vigenere(file_name, key, matrix))
    write_file(decV, decrypt_msg_by_vigenere(encV, key, matrix))

    preview_files(file_name, encV, decV, lines_to_display=5)
