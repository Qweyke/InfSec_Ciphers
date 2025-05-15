import random

from auxiliary import read_file, write_file, preview_files, RU_ALPHABET_CAP, RU_ALPHABET_LOW


def generate_vigenere_matrix(toss_letters=False, capital_letters=False):
    alphabet = RU_ALPHABET_CAP if capital_letters else RU_ALPHABET_LOW
    alphabet = alphabet.copy()
    if toss_letters:
        random.shuffle(alphabet)

    v_matrix = []

    print("Vigenere matrix:")
    for i in range(len(alphabet)):
        row = alphabet[i:] + alphabet[:i]
        v_matrix.append(row)
        print(''.join(row))

    return v_matrix


def get_alphabet_and_index(char):
    alphabet = RU_ALPHABET_CAP if char.isupper() else RU_ALPHABET_LOW
    return alphabet.index(char)


def encrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix):
    original_text = read_file(file_path)

    encrypted_list = []

    current_key_pos = -1
    key_len = len(key_str)

    for char in original_text:
        if char.lower() in RU_ALPHABET_LOW:
            current_key_pos = (current_key_pos + 1) % key_len
            key_letter = key_str[current_key_pos]

            char_index = get_alphabet_and_index(char)
            key_index = get_alphabet_and_index(key_letter)

            encrypted_char = v_matrix[key_index][char_index]
            if char.isupper():
                encrypted_char = encrypted_char.upper()
            encrypted_list.append(encrypted_char)
        else:
            encrypted_list.append(char)

    return ''.join(encrypted_list)


def decrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix):
    original_text = read_file(file_path)

    decrypted_list = []

    current_key_pos = -1
    key_len = len(key_str)

    for char in original_text:
        if char.lower() in RU_ALPHABET_LOW:
            current_key_pos = (current_key_pos + 1) % key_len
            key_letter = key_str[current_key_pos]

            key_index = get_alphabet_and_index(key_letter)
            alphabet = RU_ALPHABET_CAP if char.isupper() else RU_ALPHABET_LOW
            row = v_matrix[key_index]
            col_index = row.index(char.lower())
            decrypted_char = alphabet[col_index]
            if char.isupper():
                decrypted_char = decrypted_char.upper()

            decrypted_list.append(decrypted_char)
        else:
            decrypted_list.append(char)

    return ''.join(decrypted_list)


if __name__ == "__main__":
    file_name = "test.txt"
    encV = f"encV_{file_name}"
    decV = f"decV_{file_name}"

    key = "ключ"

    matrix = generate_vigenere_matrix(toss_letters=False, capital_letters=False)
    write_file(encV, encrypt_msg_by_vigenere(file_name, key, matrix))
    write_file(decV, decrypt_msg_by_vigenere(encV, key, matrix))

    preview_files(file_name, encV, decV, lines_to_display=5)
