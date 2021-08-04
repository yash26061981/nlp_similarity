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


class Params:
    def __init__(self):
        self.best_th = 0.8
        self.num_word_match_th = 0.75
        self.rhyme_pass_word_len = 6
        self.string_overlap_th = 0.65
        self.fuzzy_match_th = 0.7
        self.hybrid_match_alternate_threshold = 0.75
        self.avg_list_overlap_score = 0.4
        self.enable_rhyme = False
        self.get_best_match = True
        # self.use_aggresive_partial_match = False  #True
        self.reject_syn_ant_match = True
        self.reject_word_forms = False
        self.remove_stop_words = False
        pass
