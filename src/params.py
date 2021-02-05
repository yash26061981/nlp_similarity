#!/usr/bin/python


class Params:
    def __init__(self):
        self.num_word_match_th = 0.75
        self.rhyme_pass_word_len = 6
        self.string_overlap_th = 0.65
        self.enable_rhyme = False
        self.get_best_match = True
        self.use_aggresive_partial_match = True
        self.best_th = 0.8
        self.avg_list_overlap_score = 0.4
        self.reject_syn_ant_match = True
        self.reject_word_forms = True
        print('Loaded RunTime Parameters')
        pass