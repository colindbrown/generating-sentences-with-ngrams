from nltk.corpus import brown
from nltk import trigrams
from collections import defaultdict
import random

scifi_trigram_model = defaultdict(lambda: defaultdict(lambda: 0))

# break into trigrams
scifi_tris = []
for sent in brown.sents(categories=["science_fiction"]):
    scifi_tris += list(trigrams(sent, pad_left=True, pad_right=True))

# create dictionary of dictionaries for trigam counting
for tri in scifi_tris:
    scifi_trigram_model[(tri[0], tri[1])][tri[2]] += 1

# convert to probabilities
for key in scifi_trigram_model:
    count = sum(scifi_trigram_model[key].values())
    for third in scifi_trigram_model[key]:
        scifi_trigram_model[key][third] /= count

# initialize sentence
gen_text = [None, None]
while True:
    threshold = random.random()
    prob_sum = .0
    prev = (gen_text[-2], gen_text[-1])

    # add word to sentence if sum of probs is greater than random threshold
    for word, prob in scifi_trigram_model[prev].items():
        prob_sum += prob

        if prob_sum >= threshold:
            gen_text.append(word)
            break

    # detect end of sentence
    if gen_text[-2:] == [None, None]:
        break

print(" ".join(gen_text[2:-2]))