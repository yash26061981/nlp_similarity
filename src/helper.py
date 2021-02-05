#!/usr/bin/python
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("../..")))
import math
import nltk
import inflect
import numpy as np
from word2number import w2n
from nltk.corpus import wordnet
from pyinflect import getAllInflections, getInflection


class Helper:
    def __init__(self):
        self.use_stopwords_lib = nltk.corpus.stopwords.words('english')
        self.use_tokenize = nltk.tokenize.word_tokenize
        self.synantnet = wordnet.synsets
        self.inflect_engine = inflect.engine()
        self.w2n_engine = w2n
        pass

    def word_tokenize(self, input_sentence):
        return self.use_tokenize(input_sentence)

    def remove_stop_words(self, input_word_token):
        return {word for word in input_word_token if not word in self.use_stopwords_lib}

    def tokenize_and_remove_stopwords(self, word_list):
        word_token = [self.word_tokenize(word) for word in word_list]
        filtered = [" ".join([word for word in token if not word in self.use_stopwords_lib]) for token in word_token]
        return filtered

    @staticmethod
    def get_vectors(dict_set, input_dict):
        vector = []
        for uv in dict_set:
            value = 1 if uv in input_dict else 0
            vector.append(value)
        return vector

    def convert_number_to_words(self, string, group=0):
        num = self.inflect_engine.number_to_words(string, group=group)
        num = num.replace(",", "").replace("-", " ")
        return num

    def get_additional_numberwords(self, string):
        additional_group, str1_group, str2_group = [], [], []
        str1 = string[0:-3]
        min_iter1 = min(3, len(str1))
        str2 = string[-3::]
        min_iter2 = min(3, len(str2))
        for i in range(min_iter1 + 1):
            word = self.convert_number_to_words(str1, group=i)
            str1_group.append(word)
        for i in range(min_iter2 + 1):
            word = self.convert_number_to_words(str2, group=i)
            str2_group.append(word)
        for g1 in np.unique(str1_group):
            for g2 in np.unique(str2_group):
                g = g1 + ' ' + g2
                additional_group.append(g)
        return additional_group

    def get_group_of_numberwords(self, string):
        group = []
        max_p_and_c = min(3, len(string))
        for i in range(max_p_and_c + 1):
            word = self.convert_number_to_words(string, group=i)
            group.append(word)

        if len(string) > 4:
            group += self.get_additional_numberwords(string)
        return np.unique(group)

    def convert_words_to_number(self, word):
        num = None
        try:
            num = self.w2n_engine.word_to_num(word)
        except ValueError:
            return False, num
        else:
            return True, num

    def convert_word_to_vectors(self, input_1, input_2):
        input_1_token = self.word_tokenize(input_1)
        input_2_token = self.word_tokenize(input_2)

        input_1_dict = self.remove_stop_words(input_1_token)
        input_2_dict = self.remove_stop_words(input_2_token)

        union_set = input_1_dict.union(input_2_dict)

        input_1_vect = self.get_vectors(union_set, input_1_dict)
        input_2_vect = self.get_vectors(union_set, input_2_dict)
        return union_set, input_1_vect, input_2_vect

    def get_number_and_words_of_digits(self, word, is_digit):
        if is_digit:
            ans_digit = float(word)
            ans_words = self.get_group_of_numberwords(word)
            return ans_digit, ans_words, True
        else:
            is_number, ans_digit = self.convert_words_to_number(word)
            if not is_number:
                return None, None, False
            ans_digit = float(ans_digit)
            ans_words = [word]
            return ans_digit, ans_words, True

    def get_synonyms_antonyms(self, word):
        synonyms, antonyms = [], []
        for syn in self.synantnet(word):
            for lm in syn.lemmas():
                synonyms.append(lm.name())
                if lm.antonyms():
                    antonyms.append(lm.antonyms()[0].name())
        return synonyms, antonyms

    @staticmethod
    def get_word_forms(word):
        forms = getAllInflections(word)
        forms_list = [list(v)[0] for k,v in forms.items()]
        # print(forms_list)
        return forms_list

    def check_if_set_subset_in_options(self, options):
        option_list = [list(self.remove_stop_words(opt).values()) for opt in options]


if __name__ == '__main__':
    util = Helper()
    util.get_word_forms('angry')
    print('done')
