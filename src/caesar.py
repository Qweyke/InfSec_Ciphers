from auxiliary import read_file, write_file, preview_files, RU_ALPHABET_CAP, RU_ALPHABET_LOW


def shift_char_caesar(char, shift_key):
    if char.isupper():
        alphabet = RU_ALPHABET_CAP
    else:
        alphabet = RU_ALPHABET_LOW

    if char in alphabet:
        old_index = alphabet.index(char)
        new_index = (old_index + shift_key) % len(alphabet)
        return alphabet[new_index]
    else:
        return char


def encrypt_msg_by_caesar(file_path, shift_key):
    original_text = read_file(file_path)
    encrypted_list = [shift_char_caesar(char, shift_key) for char in original_text]
    return ''.join(encrypted_list)


def decrypt_msg_by_caesar(file_path, shift_key):
    return encrypt_msg_by_caesar(file_path, -shift_key)


if __name__ == "__main__":
    file_name = "test.txt"
    encC = f"encC_{file_name}"
    decC = f"decC_{file_name}"
    shift = 3

    write_file(encC, encrypt_msg_by_caesar(file_name, shift))
    write_file(decC, decrypt_msg_by_caesar(encC, shift))
    preview_files(file_name, encC, decC, lines_to_display=5)
