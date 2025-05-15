from auxiliary import read_file, write_file, preview_files, LATIN_ALP_LEN


def encrypt_msg_by_caesar(file_path, shift_key):
    original_text = read_file(file_path)
    encrypted_list = []
    for char in original_text:
        if char.isalpha():
            first_letter_in_ascii = 'A' if char.isupper() else 'a'
            old_char_pos = ord(char) - ord(first_letter_in_ascii)
            new_char_pos = (old_char_pos + shift_key) % LATIN_ALP_LEN
            encrypted_list.append(chr(new_char_pos + ord(first_letter_in_ascii)))
        else:
            encrypted_list.append(char)

    encrypted_text = ''.join(encrypted_list)
    return encrypted_text

def decrypt_msg_by_caesar(file_path, shift_key):
    return encrypt_msg_by_caesar(file_path, -1 * shift_key)

if __name__ == "__main__":
    file_name = "test.txt"
    encC = f"encC_{file_name}"
    decC = f"decC_{file_name}"
    shift = 3


    write_file(encC,  encrypt_msg_by_caesar(file_name, shift))
    write_file(decC,  decrypt_msg_by_caesar(encC, shift))
    preview_files(file_name, encC, decC, lines_to_display=5)
