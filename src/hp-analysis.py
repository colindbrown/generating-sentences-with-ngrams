from ngram_text import *
from text_standardization import *

NGRAM_SIZE = 3
NUM_GEN = 3

files = {
    "Harry Potter and the Sorcerer's Stone": "files/hp1.txt",
    "Harry Potter and the Chamber of Secrets": "files/hp2.txt",
    "Harry Potter and the Prisoner of Azkaban": "files/hp3.txt",
    "Harry Potter and the Goblet of Fire": "files/hp4.txt",
    "Harry Potter and the Order of the Phoenix": "files/hp5.txt",
    "Harry Potter and the Half-Blood Prince": "files/hp6.txt",
    "Harry Potter and the Deathly Hallows": "files/hp7.txt"
}

for title, path in files.items():
    text = load_standardized_text(path)
    model = NgramText(title, text, NGRAM_SIZE)

    print("\n", title, ":\n")
    print(model.generate_text(), "\n")
    print(model.generate_max(), "\n")