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


class Result:
    def __init__(self, match_score=0.0, match_method='None', is_similar=False,
                 skip_match=False, match_word='None', processed=False, actual_answer='None', entered_ans=None,
                 true_alternatives='None', other_options='None'):
        self.score = match_score
        self.match_method = match_method
        self.is_similar = is_similar
        self.skip_match = skip_match
        self.match_word = match_word
        self.processed = processed
        self.actual_answer = actual_answer
        if entered_ans is None:
            self.entered_ans = []
        else:
            self.entered_ans = entered_ans
        self.true_alternatives = true_alternatives
        self.other_options = other_options
        pass
