#!/usr/bin/python
# -*- coding: utf-8 -*-


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
