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

from ..nlpsim_utils.utilities import *
from ..nlpsim_utils.helper import *
from ..nlpsim_main.params import *
from ..nlpsim_main.input_class import *


class ProcessArgs:
    def __init__(self, logger, threshold):
        self.config = Params()
        self.utils = Utilities()
        self.helper = Helper()
        self.threshold = threshold
        self.logger = logger
        pass

    def parse_and_check_args(self, **kwargs):
        raw_args = self.parse_args(**kwargs)
        if raw_args.actual_answer is None or raw_args.utterance_answer is None:
            return raw_args, None, None, None

        self.log_inputs('Raw ARgs:           ', raw_args)
        processed_args = self.process_args(raw_args)
        if self.config.remove_stop_words:
            nlp_processed_args = self.remove_stopwords_from_args(processed_args)
        else:
            nlp_processed_args = processed_args
        self.log_inputs('NLP Processed ARgs: ', nlp_processed_args)

        filtered_args = self.filter_common_words_from_options(nlp_processed_args)
        self.log_inputs('Filtered ARgs:      ', filtered_args)

        final_args = self.run_sanity_check(args=self.utils.clone(filtered_args))
        self.log_inputs('Final ARgs:         ', final_args)

        if self.config.filter_repeated_words and final_args.utterance_answer is not None:
            self.filter_repeated_words_from_utterances(final_args)

        return raw_args, processed_args, filtered_args, final_args

    def parse_args(self, **kwargs):
        try:
            s1 = kwargs.get('s1')
            s2 = kwargs.get('s2')
            s1 = s1 if len(s1) > 0 else None
            s2 = s2 if len(s2) > 0 else None
        except:
            self.logger.log_error('Got Input Error Exception')
            return Input()

        if kwargs.get('th') is not None:
            th = kwargs.get('th')
        else:
            th = self.threshold

        if kwargs.get('s3') is not None:
            s3 = kwargs.get('s3')
            s3 = s3 if len(s3) > 0 else None
        else:
            s3 = None
        if kwargs.get('s4') is not None:
            s4 = kwargs.get('s4')
            s4 = s4 if len(s4) > 0 else None
        else:
            s4 = None
        if kwargs.get('q_id') is not None:
            q_id = kwargs.get('q_id')
        else:
            q_id = None
        if kwargs.get('agg_th') is not None:
            agg_th = kwargs.get('agg_th')
        else:
            agg_th = False

        return Input(actual_answer=s1, utterance_answer=s2, correct_ans_variances=s3,
                     other_options=s4, threshold=th, quest_id=q_id, aggresive_th=agg_th)

    def log_inputs(self, s, args):
        text = '{}::: S1- {}, S2- {}, S3- {}, S4- {}'.format(s, args.actual_answer, args.utterance_answer,
                                                             args.correct_ans_variances, args.other_options)
        self.logger.log_debug(text)

    def process_args(self, args):
        p_args = self.utils.clone(args)
        p_args.actual_answer = self.utils.get_list_from_str(args.actual_answer, get_list=False)
        p_args.utterance_answer = self.utils.get_list_from_str(args.utterance_answer, get_list=True)
        p_args.correct_ans_variances = self.utils.get_list_from_str(args.correct_ans_variances, get_list=True) \
            if args.correct_ans_variances is not None else None
        p_args.other_options = self.utils.get_list_from_str(args.other_options, get_list=True) \
            if args.other_options is not None else None

        act_len = len(p_args.actual_answer.split(' '))
        if act_len <= 3 and not p_args.aggresive_th:
            p_args.aggresive_th = True
            self.logger.log_info('Using Aggressive Thresholding')
        return p_args

    def filter_common_words_from_options(self, args):
        if args.other_options and self.utils.are_removal_common_words_required(
                [args.actual_answer] + args.other_options):
            filtered_args = self.utils.clone(args)
            have_common_words, common_words = self.utils.get_common_words_in_options(filtered_args)
            if have_common_words:
                act_ans_new = self.utils.remove_common_words(filtered_args.actual_answer, common_words)
                act_ans_new = act_ans_new if len(act_ans_new) > 0 else None
                filtered_utterances = []
                for u_sentence in args.utterance_answer:
                    utt_ans_new = self.utils.remove_common_words(u_sentence, common_words)
                    if utt_ans_new == u_sentence:
                        utt_ans_new = self.helper.get_non_matched_string(u_sentence, common_words)
                    utt_ans_new = utt_ans_new if len(utt_ans_new) > 0 else None
                    if utt_ans_new:
                        filtered_utterances.append(utt_ans_new)
                filtered_args.actual_answer = act_ans_new
                filtered_args.utterance_answer = filtered_utterances
            return filtered_args
        else:
            return args

    def remove_stopwords_from_args(self, args):
        p_args = self.utils.clone(args)
        o_filtered = self.helper.tokenize_and_remove_stopwords(args.other_options) \
            if args.other_options else args.other_options
        u_filtered = self.helper.tokenize_and_remove_stopwords(args.utterance_answer)
        a_filtered = self.helper.tokenize_and_remove_stopwords([args.actual_answer])
        v_filtered = self.helper.tokenize_and_remove_stopwords(args.correct_ans_variances) \
            if args.correct_ans_variances else args.correct_ans_variances
        p_args.actual_answer = a_filtered[0]
        p_args.other_options = o_filtered
        p_args.utterance_answer = u_filtered
        p_args.correct_ans_variances = v_filtered
        return p_args

    def run_sanity_check(self, args):
        args.actual_answer = self.utils.run_sanity_check(args.actual_answer, islist=False)
        args.utterance_answer = self.utils.run_sanity_check(args.utterance_answer)
        args.correct_ans_variances = self.utils.run_sanity_check(args.correct_ans_variances)
        args.other_options = self.utils.run_sanity_check(args.other_options)
        return args

    def filter_repeated_words_from_utterances(self, args):
        args.utterance_answer = self.utils.filter_repeated_words(args.utterance_answer)
