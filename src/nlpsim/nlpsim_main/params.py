#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.use_aggresive_partial_match = True
        self.reject_syn_ant_match = True
        self.reject_word_forms = False
        self.remove_stop_words = False
        pass
