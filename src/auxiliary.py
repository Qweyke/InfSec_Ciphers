
LATIN_ALP_LEN = 26

def read_file(file_path):
    with open(f'../{file_path}', 'r', encoding='utf-8') as opened_file:
        return opened_file.read()

def write_file(file_path, text):
    with open(f'../{file_path}', 'w', encoding='utf-8') as opened_file:
        opened_file.write(text)


def preview_files(*filenames, lines_to_display=5):
    for f_name in filenames:
        print(f"\n--- {f_name} ---")
        with open(f'../{f_name}', encoding='utf-8') as f:
            for _ in range(lines_to_display):
                print(f.readline().strip(), end='')
        print()