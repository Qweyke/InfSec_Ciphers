import random
from collections import Counter

from auxiliary import read_file, write_file, preview_files, RU_ALPHABET_CAP, RU_ALPHABET_LOW
from src.freq_analyzer import normalize_text


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
        print(row)

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


def crack_vigenere_cipher(file_path: str, v_matrix):
    def calculate_coincidence_index(text):
        norm_text = normalize_text(text)
        norm_text_len = len(norm_text)
        freqs = Counter(norm_text)

        for letter, freq in freqs:


        return sum(f * (f - 1) for f in freqs.values()) / (text_len * (text_len - 1)) if text_len > 1 else 0

    def find_key_length(text, max_key_len=20):
        text = [c for c in text if c in RU_ALPHABET_LOW]
        avg_ics = []
        for key_len in range(1, max_key_len + 1):
            ics = []
            for i in range(key_len):
                group = text[i::key_len]
                ic = index_of_coincidence(group)
                ics.append(ic)
            avg_ics.append((key_len, sum(ics) / len(ics)))
        likely_key_len = max(avg_ics, key=lambda x: x[1])[0]
        print("Average ICs by key length:", avg_ics)
        print(f"Likely key length: {likely_key_len}")
        return likely_key_len

    def split_text_by_key_length(text, key_len):
        return [text[i::key_len] for i in range(key_len)]

    def guess_key(text, key_len):
        text = [c for c in text if c in RU_ALPHABET_LOW]
        groups = split_text_by_key_length(text, key_len)
        v_key = ''

        # Частая буква — 'о'
        common_letter = 'о'
        ru_index = RU_ALPHABET_LOW.index(common_letter)

        for group in groups:
            if not group:
                v_key += 'а'  # fallback
                continue
            freqs = Counter(group)
            most_common_letter = freqs.most_common(1)[0][0]
            letter_index = RU_ALPHABET_LOW.index(most_common_letter)
            shift = (letter_index - ru_index) % len(RU_ALPHABET_LOW)
            key_letter = RU_ALPHABET_LOW[shift]
            v_key += key_letter
        return v_key

    encrypted_text = read_file(file_path)
    key_len = find_key_length(encrypted_text)
    v_key = guess_key(encrypted_text, key_len)

    # Дешифруем, передав текст как файл
    decrypted = decrypt_msg_by_vigenere(file_path, v_key, v_matrix)
    print(f"Guessed key: {v_key}")
    return decrypted


if __name__ == "__main__":
    file_name = "test.txt"
    encV = f"encV_{file_name}"
    decV = f"decV_{file_name}"
    crkV = f"crkV_{file_name}"

    key = "ключ"
    matrix = generate_vigenere_matrix(toss_letters=False, capital_letters=False)

    write_file(encV, encrypt_msg_by_vigenere(file_name, key, matrix))
    write_file(decV, decrypt_msg_by_vigenere(encV, key, matrix))
    write_file(crkV, crack_vigenere_cipher(encV, matrix))

    preview_files(file_name, encV, decV, crkV, lines_to_display=5)
