from auxiliary import read_file, write_file, preview_files, RU_ALPHABET_CAP, RU_ALPHABET_LOW
from src.freq_analyzer import normalize_text, count_letter_frequencies, analyze_text_file


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


def crack_caesar_cipher(file_path):
    encrypted_text = read_file(file_path)
    norm_text = normalize_text(encrypted_text)

    enc_letter_freq = count_letter_frequencies(norm_text)
    most_common_letter = enc_letter_freq.most_common(1)[0][0]
    most_common_letter_index = RU_ALPHABET_LOW.index(most_common_letter)

    ru_letter_freq, _ = analyze_text_file("big_russian.txt")
    most_common_ru_letter = ru_letter_freq.most_common(1)[0][0]
    most_common_ru_letter_index = RU_ALPHABET_LOW.index(most_common_ru_letter)

    shift_key = abs((most_common_letter_index - most_common_ru_letter_index) % len(RU_ALPHABET_CAP))

    decrypted_text = decrypt_msg_by_caesar(file_path, shift_key)
    print(f"Key shift cracked: {shift_key}")
    return decrypted_text


if __name__ == "__main__":
    file_name = "test.txt"
    encC = f"encC_{file_name}"
    decC = f"decC_{file_name}"
    crkC = f"crkC_{file_name}"

    shift = 3

    write_file(encC, encrypt_msg_by_caesar(file_name, shift))
    write_file(decC, decrypt_msg_by_caesar(encC, shift))
    write_file(crkC, crack_caesar_cipher(encC))

    preview_files(file_name, encC, decC, crkC, lines_to_display=5)
