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


class Input:
    def __init__(self, actual_answer=None, utterance_answer=None,
                 correct_ans_variances=None, other_options=None, threshold=0.0, method='None', quest_id=None,
                 aggresive_th=False):
        self.actual_answer = actual_answer
        self.utterance_answer = utterance_answer
        self.correct_ans_variances = correct_ans_variances
        self.other_options = other_options
        self.threshold = threshold
        self.method = method
        self.quest_id = quest_id
        self.aggresive_th = aggresive_th
        pass