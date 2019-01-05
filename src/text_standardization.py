import string

def valid_line(line):
    line = line.strip()
    if not line or line[0].isdigit(): # reject empty lines and page numbers
        return False
    elif line.lower().startswith("chapter"): # reject chapter titles
        return False
    return True
    

def load_standardized_text(path):
    with open(path) as file_text:
        # strip whitespace around lines, reject non-text lines
        lines = [line.strip() for line in file_text if valid_line(line)]

        # remove non-ascii characters
        valid_chars = set(string.printable)
        filtered_text = "".join(filter(lambda x: x in valid_chars, " ".join(lines)))
        return filtered_text
