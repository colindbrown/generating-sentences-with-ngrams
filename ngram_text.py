from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import random

class NgramText:
    def __init__(self, title, full_text, n=3):
        self.title = title
        self.sentences = self.sentence_format(full_text)
        self.ngram_size = n
        self.ngram_model = self.create_ngram_model(n)

    def sentence_format(self, text):
        sent_strs = sent_tokenize(text)
        sents = []
        for sent in sent_strs:
            sents.append(word_tokenize(sent))
        return sents

    def create_ngram_model(self, n):
        # generate ngrams
        ngrams_list = []
        for sent in self.sentences:
            ngrams_list += list(ngrams(sent, n, pad_left=True, pad_right=True))

        # create count of words given prior words
        ngram_model = defaultdict(lambda: defaultdict(lambda: 0))
        for ngram in ngrams_list:
            prior_words = ngram[:-1]
            next_word = ngram[-1]
            ngram_model[prior_words][next_word] += 1

        # convert to probabilities
        for prior in ngram_model:
            count = sum(ngram_model[prior].values())
            for post in ngram_model[prior]:
                ngram_model[prior][post] /= count

        return ngram_model
    
    def generate_text(self):
        n = self.ngram_size
        gen_text = [None for i in range(n-1)]
        while True:
            threshold = random.random()
            prob_sum = .0
            prior = tuple(gen_text[-(n-1):])

            # add word to sentence if sum of probs is greater than random threshold
            for word, prob in self.ngram_model[prior].items():
                prob_sum += prob

                if prob_sum >= threshold:
                    gen_text.append(word)
                    break

            # detect end of sentence
            if gen_text[-(n-1):] == [None for i in range(n-1)]:
                break

        return " ".join(gen_text[n-1:-(n-1)])