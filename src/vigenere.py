import random
from collections import Counter

from auxiliary import read_file, write_file, preview_files, RU_ALPHABET_CAP, RU_ALPHABET_LOW
from src.freq_analyzer import normalize_text, count_letter_frequencies, analyze_text_file


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


def encrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix: list[list[str]]):
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


def decrypt_msg_by_vigenere(file_path: str, key_str: str, v_matrix: list[list[str]]):
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


def crack_vigenere_cipher(file_path: str):
    def calculate_coincidence_index(text_block: str) -> float:
        freqs = Counter(text_block)
        norm_text_len = len(text_block)

        conc_index = 0
        for letter in freqs:
            conc_index += (freqs[letter] / norm_text_len) * (freqs[letter] / norm_text_len)

        return conc_index

    def calculate_key_length(normalized_text: str, key_len_limit: int = 20):
        ci_plain_text = calculate_coincidence_index(read_file("big_russian.txt"))
        ci_poly_encrypted_text = calculate_coincidence_index(read_file("encV_test.txt"))
        print(
            f"CI for plain cyrillic alphabet: {ci_plain_text}, CI for poly alphabet encrypted text: {ci_poly_encrypted_text}")

        # Gather all CI for key_len in range key_len_limit
        overall_ci_list: dict[str: float] = {}
        for key_len in range(1, key_len_limit + 1):

            # Calculate each key len for current i-value
            len_goups_ci_list: list[float] = []

            # Start from first text letter with shift of key_len = 1 and so on
            for shift_val in range(key_len):
                symbol_block: str = normalized_text[shift_val::key_len]
                key_len_group_ci: float = calculate_coincidence_index(symbol_block)
                len_goups_ci_list.append(key_len_group_ci)

            curr_len_final_ci = sum(len_goups_ci_list) / key_len
            overall_ci_list[key_len] = curr_len_final_ci

        for key_len, ci_value in overall_ci_list.items():
            threshold = (ci_plain_text + ci_poly_encrypted_text) / 2
            if ci_value > threshold:
                print(f"Key len {key_len} with CI = {ci_value}, threshold = {threshold}")
                return key_len

    def decrypt_key(key_len: int, normalized_text: str):
        blocks = []
        for i in range(key_len):
            block = normalized_text[i::key_len]
            blocks.append(block)

        ru_letter_freq, _ = analyze_text_file("big_russian.txt")
        most_common_ru_letter = ru_letter_freq.most_common(1)[0][0]
        most_common_ru_letter_index = RU_ALPHABET_LOW.index(most_common_ru_letter)

        key_str = []
        for block in blocks:
            enc_letter_freq = count_letter_frequencies(block)
            most_common_letter = enc_letter_freq.most_common(1)[0][0]
            most_common_letter_index = RU_ALPHABET_LOW.index(most_common_letter)
            letter_pos = (most_common_letter_index - most_common_ru_letter_index) % len(RU_ALPHABET_CAP)

            key_str.append(RU_ALPHABET_LOW[letter_pos])

        return ''.join(key_str)

    # Extract data from text
    encrypted_text = read_file(file_path)
    # Normalize, trim etc...
    norm_text = normalize_text(encrypted_text)
    # Find key len
    k_len = calculate_key_length(normalized_text=norm_text)
    # Find key val
    key_found = decrypt_key(k_len, norm_text)
    print(f"Found key: {key_found}")
    return key_found


if __name__ == "__main__":
    file_name = "test.txt"
    encV = f"encV_{file_name}"
    decV = f"decV_{file_name}"
    crkV = f"crkV_{file_name}"

    key = "лор"
    matrix = generate_vigenere_matrix(toss_letters=False, capital_letters=False)

    write_file(encV, encrypt_msg_by_vigenere(file_name, key, matrix))
    write_file(decV, decrypt_msg_by_vigenere(encV, key, matrix))

    cracked_key = crack_vigenere_cipher(encV)
    write_file(crkV, decrypt_msg_by_vigenere(encV, cracked_key, matrix))

    preview_files(file_name, encV, decV, crkV, lines_to_display=5)
