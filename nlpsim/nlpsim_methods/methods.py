#!/usr/bin/python
import os
import sys
from pathlib import Path  # path tricks so we can import wherever the module is
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("../..")))
from nlpsim_methods.rhyming import *
from nlpsim_utils.utilities import *
from nlpsim_utils.helper import *

import re
import difflib
from difflib import SequenceMatcher
from decimal import Decimal
from fuzzywuzzy import fuzz, process


class BaseMethods:
    def __init__(self):
        pass

    def nth_root(self, value, n_root):
        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 3)

    def square_rooted(self, x):
        return round(math.sqrt(sum([a * a for a in x])), 3)

    def cosine_similarity(self, x, y):
        numerator = sum(a * b for a, b in zip(x, y))
        denominator = self.square_rooted(x) * self.square_rooted(y)
        return round(numerator / float(denominator), 3) if denominator > 0 else 0.0

    def jaccard_similarity(self, x, y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)


class Methods:
    def __init__(self, threshold, config):
        self.threshold = threshold
        self.rhyming_words = GetRhymingWords()
        self.difflib = difflib.SequenceMatcher
        self.utils = Utilities()
        self.helper = Helper()
        self.base = BaseMethods()
        self.config = config
        pass

    def match_using_cosine_similarity(self, a_ans, u_ans, threshold):
        is_similar = False
        set_of_word, vector1, vector2 = self.helper.convert_word_to_vectors(a_ans, u_ans)
        cosine_scores = self.base.cosine_similarity(vector1, vector2)
        if cosine_scores >= threshold:
            is_similar = True
        return is_similar, cosine_scores

    def match_using_jaccard_similarity(self, a_ans, u_ans, threshold):
        is_similar = False
        jacard_score = self.base.jaccard_similarity(a_ans, u_ans)
        jacard_score_rev = self.base.jaccard_similarity(u_ans, a_ans)
        print('jaccard ', [a_ans], [u_ans], [jacard_score], [jacard_score_rev])
        if jacard_score >= threshold:
            is_similar = True
        return is_similar, jacard_score

    def match_using_numbers_and_words(self, args):
        actual_answer, utterance_answer = args.actual_answer, args.utterance_answer
        is_a_digit = self.utils.check_if_digit(actual_answer)
        is_u_digit = self.utils.check_if_digit(utterance_answer)
        both_are_digit = is_u_digit & is_a_digit

        if both_are_digit:
            a_ans_digit = float(actual_answer)
            u_ans_digit = float(utterance_answer)
            if a_ans_digit == u_ans_digit:
                return True, 1.0, True
            else:
                return False, 0.0, True
        else:
            a_ans_digit, a_ans_words, a_pass = self.helper.get_number_and_words_of_digits(actual_answer, is_a_digit)
            u_ans_digit, u_ans_words, u_pass = self.helper.get_number_and_words_of_digits(utterance_answer, is_u_digit)
            if a_ans_digit is None and u_ans_digit is None:
                return False, 0.0, False
            if a_ans_digit == u_ans_digit:
                return True, 1.0, True
            if a_pass & u_pass:
                match_words = list(set(a_ans_words).intersection(set(u_ans_words)))
                if match_words:
                    return True, 1.0, True
                else:
                    a_ans_all_words = " ".join(a_ans_words)
                    u_ans_all_words = " ".join(u_ans_words)
                    is_similar, word_match_score = \
                        self.match_using_cosine_similarity(a_ans_all_words, u_ans_all_words, args.threshold)
                    if is_similar:
                        return True, word_match_score, True
                    else:
                        return False, word_match_score, True
            else:
                return False, 0.0, False

    def match_using_hybrid_num_letters(self, args):
        actual_answer, utterance_answer = args.actual_answer, args.utterance_answer
        is_a_digit = self.utils.check_if_digit(actual_answer)
        is_u_digit = self.utils.check_if_digit(utterance_answer)
        if is_a_digit and not is_u_digit: # example 20 and 20 Lacs
            u_digits = re.findall('[0-9]+', utterance_answer)
            index = [i for i, j in enumerate(u_digits) if j == actual_answer]
            if index:
                return True, 1.0, u_digits[index[0]], True
            else:
                return False, 0.0, None, True
        return False, 0.0, None, False

    def match_using_hybrid_num_letters_alternate_1(self, args):
        actual_answer, utterance_answer, threshold = args.actual_answer, args.utterance_answer, args.threshold
        a_val_list = actual_answer.split()
        u_val_list = utterance_answer.split()
        if len(a_val_list) == len(u_val_list):
            match = [False] * len(a_val_list)
            is_a_digit_list = [self.utils.check_if_digit(a_val) for a_val in a_val_list]
            is_u_digit_list = [self.utils.check_if_digit(u_val) for u_val in u_val_list]
            index, pass_index = 0, 0
            for is_a_digit, is_u_digit, a_val, u_val in zip(is_a_digit_list, is_u_digit_list, a_val_list, u_val_list):
                if is_a_digit and not is_u_digit:
                    a_words_list = self.helper.get_all_forms_of_number_to_words(a_val)
                    if u_val in a_words_list:
                        match[index] = True
                        pass_index += 1
                elif not is_a_digit and is_u_digit:
                    u_words_list = self.helper.get_all_forms_of_number_to_words(u_val)
                    if a_val in u_words_list:
                        match[index] = True
                        pass_index += 1
                else:
                    if a_val == u_val:
                        match[index] = True
                        pass_index += 1
                index += 1
            pass_score = float(pass_index)/len(match)
            if pass_score > threshold:
                return True, pass_score, True
            else:
                return False, pass_score, False
        return False, 0.0, False

    def match_using_hybrid_num_letters_alternate_2(self, args):
        actual_answer, utterance_answer, threshold = args.actual_answer, args.utterance_answer, args.threshold
        a_words = self.helper.get_all_forms_of_number_to_words_inhouse(actual_answer)
        u_words = self.helper.get_all_forms_of_number_to_words_inhouse(utterance_answer)
        print(a_words, utterance_answer, u_words, actual_answer)
        is_similar1, word_match_score1 = \
            self.match_using_cosine_similarity(a_words, utterance_answer, args.threshold)
        is_similar2, word_match_score2 = \
            self.match_using_cosine_similarity(u_words, actual_answer, args.threshold)
        if is_similar1 or is_similar2:
            return True, max(word_match_score1, word_match_score2), True
        else:
            return False, min(word_match_score1, word_match_score2), False

    @staticmethod
    def get_non_matched_string(word1, matched_word):
        matched_sent = ' '.join(matched_word).strip()
        match_blocks = SequenceMatcher(None, word1, matched_sent).get_matching_blocks()
        for block in match_blocks:
            if block.size > 0:
                overlap_word = word1[block.a:block.a + block.size]
                if overlap_word == matched_sent:
                    filtered_word = re.sub(overlap_word, "", word1)
                    return filtered_word
        return word1

    #TODO
    def match_using_string_overlap(self, a_ans, u_ans, threshold):
        '''
        partial_match = self.difflib(None, a_ans, u_ans)
        a_cop, u_cop = a_ans, u_ans
        a_cop, u_cop = a_cop.split(' '), u_cop.split(' ')

        max_len = min(len(a_cop), len(u_cop))
        ov_l = []
        for i in range(max_len):
            pos_a, pos_b, size = partial_match.find_longest_match(0, len(a_ans), i, len(u_ans))
            overlap_word = a_ans[pos_a:pos_a + size]
            ov_l += overlap_word

        ov_w = "".join(ov_l)
        '''
        ov_l, ov_t = [], []
        match_blocks = SequenceMatcher(None, a_ans, u_ans).get_matching_blocks()
        for block in match_blocks:
            overlap_word = a_ans[block.a:block.a + block.size]
            ov_l += ' ' + overlap_word

        ov_w = "".join(ov_l)
        ov_w = ov_w.lstrip().rstrip()
        difflib_score = SequenceMatcher(None, a_ans, u_ans).ratio()
        #difflib_score_rev = SequenceMatcher(None, u_ans, a_ans).ratio()
        #print(a_ans, u_ans, difflib_score, difflib_score_rev)
        overlap_scores = self.get_score_overlap_wise(a_ans, ov_w)
        avg_ov_score = sum(overlap_scores)/len(overlap_scores)
        #print([a_ans], [u_ans], [ov_w], overlap_scores, [avg_ov_score], [difflib_score], [difflib_score_rev])
        if difflib_score >= threshold:
            if self.config.use_aggresive_partial_match:
                if self.config.avg_list_overlap_score <= avg_ov_score:
                    return True, difflib_score, ov_w
                else:
                    return False, avg_ov_score, ov_w
            return True, difflib_score, ov_w
        return False, difflib_score, ov_w

    @staticmethod
    def get_score_overlap_wise(a_ans, ov_w):
        ov_w_lst = ov_w.split(' ')
        score = list()
        for val in ov_w_lst:
            score.append(SequenceMatcher(None, a_ans, val).ratio())
        return score

    def match_using_rhyming_words(self, a_ans, u_ans, threshold, best_match=False):
        score = 0.0
        is_similar = False
        if self.rhyming_words.check_if_rhyming(a_ans, u_ans):
            return True, 1,0, u_ans
        else:
            return False, 0.0, u_ans

    @staticmethod
    def is_direct_match(args):
        index = [i for i, j in enumerate(args.utterance_answer) if j == args.actual_answer]
        if index:
            return True, 1.0, args.utterance_answer[index[0]]
        else:
            if args.correct_ans_variances is not None:
                index = [i for i, j in enumerate(args.utterance_answer) if j in args.correct_ans_variances]
                if index:
                    return True, 1.0, args.utterance_answer[index[0]]
            return False, 0.0, None

    def check_if_other_options_answered(self, args):
        oth_opt_token = [self.helper.word_tokenize(oth) for oth in args.other_options]
        ut_token = [self.helper.word_tokenize(ut) for ut in args.utterance_answer]

        if self.config.remove_stop_words:
            oth_opt_dict = [list(self.helper.remove_stop_words(token)) for token in oth_opt_token]
            ut_dict = [list(self.helper.remove_stop_words(token))for token in ut_token]
        else:
            oth_opt_dict = oth_opt_token
            ut_dict = ut_token

        o_set = set(tuple(i) for i in oth_opt_dict)
        u_set = set(tuple(i) for i in ut_dict)

        if len(u_set.intersection(o_set)) > 0:
            oth_opt_word = [x[0] for x in u_set.intersection(o_set)]
            rem_utt = [utt for utt in args.utterance_answer if utt not in oth_opt_word]
            if rem_utt:
                args.utterance_answer = rem_utt
                return False, 0.0, None
            else:
                return True, 1.0, u_set.intersection(o_set)

        return False, 0.0, None

    def check_if_syn_ant_match(self, a_ans, u_ans):
        a_syn, a_ant = self.helper.get_synonyms_antonyms(a_ans)
        u_syn, u_ant = self.helper.get_synonyms_antonyms(u_ans)
        if a_ans in u_ant or u_ans in a_ant:
            return True
        return False

    def check_if_word_forms_match(self, a_ans, u_ans):
        u_ans_forms = self.helper.get_word_forms(u_ans)
        if a_ans in u_ans_forms:
            return True
        return False

    def match_using_fuzzy_logic(self, a_ans, u_ans):
        if isinstance(u_ans, list):
            #ratios = process.extract(a_ans, u_ans)
            #print(ratios)
            highest = process.extractOne(a_ans, u_ans)
            #print(highest)

        ratio = fuzz.ratio(a_ans, u_ans) * 1.0/100.0
        #partial_ratio = fuzz.partial_ratio(a_ans, u_ans)
        #token_sort_ratio = fuzz.token_sort_ratio(a_ans, u_ans)
        #token_set_ratio = fuzz.token_set_ratio(a_ans, u_ans)
        #print(a_ans, u_ans, ratio)
        #print(a_ans, u_ans, partial_ratio)
        #print(a_ans, u_ans, token_sort_ratio)
        #print(a_ans, u_ans, token_set_ratio)
        if ratio >= self.config.fuzzy_match_th:
            return True, ratio, u_ans
        return False, ratio, u_ans




if __name__ == '__main__':
    print('done')