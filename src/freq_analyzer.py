import re
from collections import Counter

import matplotlib.pyplot as plt

from auxiliary import read_file


def normalize_text(text):
    return re.sub(r'[^а-яё]', '', text.lower())


def count_letter_frequencies(text):
    return Counter(text)


def count_bigram_frequencies(text):
    bigrams = []
    for i in range(len(text) - 1):
        bigrams.append(text[i:i + 2])

    return Counter(bigrams)


def plot_top(counter, title, top_n=10):
    most_common = counter.most_common(top_n)
    labels, values = zip(*most_common)

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_top_two(counter1, title1, counter2, title2, top_n=10):
    most_common1 = counter1.most_common(top_n)
    most_common2 = counter2.most_common(top_n)

    labels1, values1 = zip(*most_common1)
    labels2, values2 = zip(*most_common2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.bar(labels1, values1, color='skyblue')
    ax1.set_title(title1)
    ax1.set_ylabel("Frequency")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    ax2.bar(labels2, values2, color='salmon')
    ax2.set_title(title2)
    ax2.set_ylabel("Frequency")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def analyze_text_file(filepath, show_output: bool = False):
    raw_text = read_file(filepath)
    normalized_text = normalize_text(raw_text)

    letter_freq = count_letter_frequencies(normalized_text)
    bigram_freq = count_bigram_frequencies(normalized_text)

    repeated_bigrams = {bg: cnt for bg, cnt in bigram_freq.items() if bg[0] == bg[1]}

    if show_output:
        print("Top 10 letters:")
        for letter, count in letter_freq.most_common(10):
            print(f"{letter}: {count}")

        print("Top 10 bigrams:")
        for bigram, count in bigram_freq.most_common(10):
            print(f"{bigram}: {count}")

        print("All bigrams with repeated letter")
        for rep, count in sorted(repeated_bigrams.items(), key=lambda x: -x[1]):
            print(f"{rep}: {count}")

        plot_top_two(letter_freq, "Top 10 letters", bigram_freq, "Top 10 bigrams")

    return letter_freq, bigram_freq


if __name__ == "__main__":
    analyze_text_file("big_russian.txt", True)
