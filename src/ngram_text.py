from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import random, string

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

    def list_to_sentence(self, word_list):
        n = self.ngram_size
        # convert list to sentence
        sentence = ""
        open_quotes = False
        no_space = False
        for i in range(n-1,len(word_list)-(n-1)):
            word = word_list[i]
            # handle spaces around quotation marks
            if word[0] == '"':
                if open_quotes:
                    open_quotes = False
                else:
                    if i >= n:
                        sentence += " "
                    no_space = True
                    open_quotes = True
            elif no_space:
                no_space = False
            # avoid spaces within tokenized words like "does n't" and before punctuation
            elif word[0] not in string.punctuation and word != "n't":
                sentence += " "
            sentence += word
        return sentence


    def generate_max(self):
        n = self.ngram_size
        gen_text = [None for i in range(n-1)]
        while True:
            prior = tuple(gen_text[-(n-1):])

            max_word = max(zip(self.ngram_model[prior].values(), self.ngram_model[prior].keys()))[1]
            gen_text.append(max_word)

            # detect end of sentence
            if gen_text[-(n-1):] == [None for i in range(n-1)] or len(gen_text) > 50:
                break

        return self.list_to_sentence(gen_text)
    
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

        return self.list_to_sentence(gen_text)