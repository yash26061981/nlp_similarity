#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 *************************************************************************
 *
 * AUDIO FIRST COMMERCE PRIVATE LIMITED Confidential
 * Copyright (c) 2020 AUDIO FIRST COMMERCE PRIVATE LIMITED.
 * All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains the property of
 * AUDIO FIRST COMMERCE PRIVATE LIMITED and its suppliers, if any. The intellectual
 * and technical concepts contained herein are proprietary to AUDIO FIRST COMMERCE
 * PRIVATE LIMITED and its suppliers and may be covered by Indian and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law. Dissemination
 * of this information or reproduction of this material is strictly forbidden unless
 * prior written permission is obtained from AUDIO FIRST COMMERCE PRIVATE LIMITED.
 *
 *************************************************************************
"""

import os
import sys
from pathlib import Path  # path tricks so we can import wherever the module is

sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("../..")))

from ..nlpsim_methods.methods import *
from ..nlpsim_utils.utilities import *
from ..nlpsim_utils.helper import *
from ..nlpsim_utils.nlp_logging import *
from ..nlpsim_main.params import *
from ..nlpsim_main.process_args import *
from ..nlpsim_main.output_class import *
from ..nlpsim_main.input_class import *


# nltk.download("stopwords")
# nltk.download('punkt')


class GetSimilarity:
    def __init__(self, cwd=None, threshold=0.4):
        self.logger = LogAppStd(cwd)
        self.config = Params()
        self.alg_to_use = AlgAbstract()
        self.utils = Utilities()
        self.helper = Helper()
        self.methods = Methods(threshold, self.config, self.logger)
        self.argparse = ProcessArgs(self.logger, threshold)
        # self.rhyming = GetRhymingWords()
        # self.threshold = threshold
        self.enable_rhyming = self.config.enable_rhyme
        self.get_best_match = self.config.get_best_match
        self.best_th = self.config.best_th
        self.reject_match_methods = ['SynAnt', 'WordForm', 'OtherOptionsAnswered']
        self.logger.log_info('Loaded RunTime Parameters')
        pass

    def use_method(self, args):
        actual_answer, utterance_answer, threshold = args.actual_answer, args.utterance_answer, args.threshold
        # self.nlpsim_methods.match_using_jaccard_similarity(actual_answer, utterance_answer, threshold)
        # Check if other options answered. If other option answered,
        # we are checking if that utterance has the correct answer or not.
        # if that has the actual + oter options, we are removing other
        # options from the utterances and keeping other sentences intact.
        if args.method == 'OtherOptionsAnswered' and self.alg_to_use.use_OtherOptionsAnswered:
            is_similar, other_option_match_score, matched_utterance = \
                self.methods.check_if_other_options_answered(args)
            return Result(match_score=other_option_match_score, match_method=args.method, is_similar=is_similar,
                          match_word=matched_utterance)

        # Checking if utterances has any one-to-one
        # match with the actual answer.
        if args.method == 'DirectMatch' and self.alg_to_use.use_DirectMatch:
            is_similar, dm_score, matched_utterance = \
                self.methods.is_direct_match(args)
            return Result(match_score=dm_score, match_method=args.method, is_similar=is_similar,
                          match_word=matched_utterance)

        elif args.method == 'NumWord' and self.alg_to_use.use_NumWord:
            is_similar, nw_score, skip_match = self.methods.match_using_numbers_and_words(args)
            return Result(match_score=nw_score, match_method=args.method, match_word=args.utterance_answer,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'HybridMatch' and self.alg_to_use.use_HybridMatch:
            is_similar, nw_score, skip_match = self.methods.match_using_hybrid_num_letters(args)
            return Result(match_score=nw_score, match_method=args.method, match_word=utterance_answer,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'SynAnt' and self.alg_to_use.use_SynAnt:
            check = self.methods.check_if_syn_ant_match(args)
            if check and not self.config.reject_syn_ant_match:
                check = False
            return Result(match_method=args.method, skip_match=check, match_word=args.utterance_answer)

        elif args.method == 'WordForm' and self.alg_to_use.use_WordForm:
            check = self.methods.check_if_word_forms_match(args)
            if check and not self.config.reject_word_forms:
                check = False
            return Result(match_method=args.method, skip_match=check, match_word=args.utterance_answer)

        elif args.method == 'Cosine' and self.alg_to_use.use_Cosine:
            is_similar, cosine_score = \
                self.methods.match_using_cosine_similarity(actual_answer, utterance_answer, threshold)
            return Result(match_score=cosine_score, match_method=args.method, is_similar=is_similar,
                          match_word=utterance_answer)

        elif args.method == 'Partial' and self.alg_to_use.use_Partial:
            is_similar, ov_score, overlap_word = \
                self.methods.match_using_string_overlap(args)
            utt_ans_overlap = utterance_answer + ' -({})'.format(overlap_word)
            return Result(match_score=ov_score, match_method=args.method,
                          is_similar=is_similar, match_word=utt_ans_overlap)

        elif args.method == 'Rhyme' and self.alg_to_use.use_Rhyme:
            is_similar, rh_score, rhyme_word = \
                self.methods.match_using_rhyming_words(actual_answer, utterance_answer, threshold, best_match=False)
            return Result(match_score=rh_score, match_method=args.method,
                          is_similar=is_similar, match_word=rhyme_word)

        elif args.method == 'FuzzyMatch' and self.alg_to_use.use_FuzzyMatch:
            is_similar, fm_score, fm_word = \
                self.methods.match_using_fuzzy_logic(args)
            return Result(match_score=fm_score, match_method=args.method,
                          is_similar=is_similar, match_word=fm_word)
        else:
            self.logger.log_error('Method {} is not supported'.format(args.method))
        return Result(processed=False)

    def find_similarity(self, args):
        score, utt_ans, method = [], [], []

        # args.threshold = self.threshold
        args.method = 'SynAnt'
        syn_ant_result = self.use_method(args)
        score.append(syn_ant_result.score), utt_ans.append(syn_ant_result.match_word)
        method.append(syn_ant_result.match_method)
        if syn_ant_result.skip_match:
            return syn_ant_result

        args.threshold = self.config.num_word_match_th
        args.method = 'NumWord'
        num_word_result = self.use_method(args)
        score.append(num_word_result.score), utt_ans.append(num_word_result.match_word)
        method.append(num_word_result.match_method)
        if num_word_result.is_similar or num_word_result.skip_match:
            return num_word_result

        args.method = 'HybridMatch'
        args.threshold = self.config.hybrid_match_alternate_threshold
        hybrid_match_result = self.use_method(args)
        score.append(hybrid_match_result.score), utt_ans.append(hybrid_match_result.match_word)
        method.append(hybrid_match_result.match_method)
        if hybrid_match_result.is_similar or hybrid_match_result.skip_match:
            return hybrid_match_result

        # args.threshold = self.threshold
        args.method = 'WordForm'
        word_form_result = self.use_method(args)
        score.append(word_form_result.score), utt_ans.append(word_form_result.match_word)
        method.append(word_form_result.match_method)
        if word_form_result.skip_match:
            return word_form_result

        args.threshold = self.config.string_overlap_th
        args.method = 'Partial'
        intersection_result = self.use_method(args)
        score.append(intersection_result.score), utt_ans.append(intersection_result.match_word)
        method.append(intersection_result.match_method)
        if intersection_result.is_similar:
            return intersection_result

        # args.threshold = self.threshold
        args.method = 'Cosine'
        cosine_result = self.use_method(args)
        score.append(cosine_result.score), utt_ans.append(cosine_result.match_word)
        method.append(cosine_result.match_method)
        if cosine_result.is_similar:
            return cosine_result

        args.method = 'FuzzyMatch'
        fuzzy_result = self.use_method(args)
        score.append(fuzzy_result.score), utt_ans.append(fuzzy_result.match_word)
        method.append(fuzzy_result.match_method)
        if fuzzy_result.is_similar:
            return fuzzy_result

        if self.enable_rhyming:
            args.threshold = self.config.string_overlap_th
            args.method = 'Rhyme'
            rhyme_result = self.use_method(args)
            score.append(rhyme_result.score), utt_ans.append(rhyme_result.match_word)
            method.append(rhyme_result.match_method)
            if rhyme_result.is_similar:
                return rhyme_result

        max_index = self.utils.get_best_match(score)
        return Result(is_similar=False, match_score=score[max_index],
                      match_word=utt_ans[max_index], match_method=method[max_index])

    def populate_payload(self, args, match_result, got_exception=False):
        if not got_exception:
            self.logger.log_info('Method: {} :: Similar: {} :: Score: {} :: Matched: {} :: QuestionID: {}'.format(
                match_result.match_method, match_result.is_similar, match_result.score,
                match_result.match_word, args.quest_id))
        match_result.actual_answer = args.actual_answer
        match_result.entered_ans = args.utterance_answer
        match_result.true_alternatives = args.correct_ans_variances
        match_result.other_options = args.other_options
        return match_result

    def get_similarity(self, **kwargs):
        try:
            raw_args, processed_args, filtered_args, final_args = self.argparse.parse_and_check_args(**kwargs)
            if raw_args.actual_answer is None or raw_args.utterance_answer is None:
                self.logger.log_error('Correct Answer/ Utterances field can not be Blank or None')
                return self.populate_payload(raw_args, Result(), got_exception=True)
            scores_list, word_list, method_list, similar_list = [], [], [], []
            utterance_answer = self.utils.clone(final_args.utterance_answer)
            try:
                if final_args.other_options:
                    final_args.method = 'OtherOptionsAnswered'
                    other_option_ans_result = self.use_method(final_args)
                    if other_option_ans_result.is_similar:
                        return self.populate_payload(processed_args, Result(match_method=final_args.method))

                final_args.method = 'DirectMatch'
                dm_result = self.use_method(final_args)

                if dm_result.is_similar:
                    return self.populate_payload(processed_args, dm_result)
                else:
                    for u_sentence in utterance_answer:
                        if u_sentence is None:
                            continue
                        final_args.utterance_answer = u_sentence
                        match_result = \
                            self.find_similarity(final_args)

                        if match_result.score >= self.best_th:
                            return self.populate_payload(processed_args, match_result)

                        if self.get_best_match:
                            scores_list.append(match_result.score)
                            word_list.append(match_result.match_word)
                            method_list.append(match_result.match_method)
                            similar_list.append(match_result.is_similar)
                        else:
                            if match_result.is_similar or match_result.skip_match:
                                return self.populate_payload(processed_args, match_result)

                    if self.get_best_match and len(scores_list) > 0:
                        max_index = self.utils.get_best_match(scores_list)
                        match_score = scores_list[max_index]
                        if match_score == 0.0 and not (method_list[max_index] in self.reject_match_methods):
                            return self.populate_payload(processed_args, Result())
                        return self.populate_payload(processed_args,
                                                     Result(is_similar=similar_list[max_index],
                                                            match_score=scores_list[max_index],
                                                            match_word=word_list[max_index],
                                                            match_method=method_list[max_index]))
                return self.populate_payload(processed_args, Result())
            except ValueError:
                self.logger.log_error('Got Value Error Exception')
                return self.populate_payload(processed_args, Result(match_method='Value Error Exception'),
                                             got_exception=True)
            except BaseException as e:
                self.logger.log_error('Got ERROR ' + str(e))
                return self.populate_payload(processed_args, Result(match_method='Got ERROR ' + str(e)),
                                             got_exception=True)
            except:
                self.logger.log_error('Got Unknown Exception')
                return self.populate_payload(processed_args, Result(match_method='Got Unknown Exception'),
                                             got_exception=True)
        except:
            self.logger.log_error('Got Unknown Exception')
            return self.populate_payload(Input(), Result(match_method='Got Unknown Exception'), got_exception=True)

    def process(self, **kwargs):
        return self.get_similarity(**kwargs)


if __name__ == '__main__':
    print('Similarity Function Called: Done')
