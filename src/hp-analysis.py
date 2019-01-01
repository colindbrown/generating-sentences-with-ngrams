from ngram_text import *

NGRAM_SIZE = 5
NUM_GEN = 3

def valid_line(line):
    line = line.strip()
    if not line or line.isdigit(): # reject empty lines and page numbers
        return False
    elif line.lower().startswith("chapter"): # reject chapter titles
        return False
    return True
    

def load_standardized_text(path):
    with open(path) as file_text:
        lines = [line.strip() for line in file_text if valid_line(line)]
        return " ".join(lines)

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