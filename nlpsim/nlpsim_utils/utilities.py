#!/usr/bin/python
import os
import sys
import math
import numpy as np
import shutil, copy


class Utilities:
    def __init__(self):
        pass

    @staticmethod
    def clone(obj):
        return copy.copy(obj)

    @staticmethod
    def create_dir_if_not_exists(parent_dir, dir, flush=False):
        path = os.path.join(parent_dir, dir)
        isdir = os.path.isdir(path)
        if isdir and not flush:
            return path
        elif isdir:
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            os.mkdir(path)
        return path

    @staticmethod
    def check_if_digit(word):
        return word.isdigit()

    @staticmethod
    def remove_braces_from_input_text(at_val):
        at_val = [v.strip().lower() for v in
                  at_val.replace('"', '').replace('.', '').lstrip('\[{').rstrip('\]}').split(',')]
        return at_val

    @staticmethod
    def remove_quotes_from_input_text(at_val):
        return at_val if isinstance(at_val, list) else at_val.replace('\'','').replace('"','')

    @staticmethod
    def remove_quotes_from_input_text_1(at_val):
        if isinstance(at_val, list):
            return at_val
        else:
            at_val_lst = [v for v in at_val if v not in ['\\', '"']]
            return "".join(at_val_lst)

    def remove_noise(self, word, get_list=False):
        word1 = self.remove_quotes_from_input_text(word)
        if isinstance(word1, list):
            word2 = [self.remove_braces_from_input_text(w) for w in word1]
        else:
            word2 = self.remove_braces_from_input_text(word1)
        if get_list:
            if not isinstance(word2, list):
                word2 = [word2]
            if len(word2) > 0:
                if any(isinstance(el, list) for el in word2):
                    word2 = word2[0]
        return word2

    @staticmethod
    def get_best_match(score):
        index_max = np.argmax(score)
        return index_max

    @staticmethod
    def get_common_words_in_options(args):
        actual_ans = args.actual_answer
        other_opt = args.other_options
        act_len = len(actual_ans.split(' '))
        if act_len > 1:
            act_list = actual_ans.split(' ')
            other_opt_list = [opt.split(' ') for opt in other_opt] if other_opt is not None else []
            common_word = []
            for opt_lst in other_opt_list:
                common_word.append(list(set(act_list).intersection(opt_lst)))
            common_word = [item for sublist in common_word for item in sublist]
            un_w = np.unique(common_word).tolist()
            if len(un_w) > 0:
                return True, un_w
        return False, None

    @staticmethod
    def remove_common_words(word1, common_word):
        word1_list = word1.split(' ')
        word1_both = set(word1_list).intersection(common_word)
        indices_word1 = [word1_list.index(x) for x in word1_both]
        [word1_list.pop(index) for index in indices_word1]
        return ' '.join(word1_list).strip()

    @staticmethod
    def is_removal_common_words_required(options):
        len_opt = [len(opt.split(' ')) for opt in options]
        if len(np.unique(len_opt).tolist()) == 1:
            return True
        return False


if __name__ == '__main__':
    utils = Utilities()
    print('done')
    istr = '"[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]"'
    nst = utils.remove_noise(istr, get_list=True)
    print(istr)
    print(nst)