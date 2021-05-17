#!/usr/bin/python
import os
import sys
from pathlib import Path  # path tricks so we can import wherever the module is

sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__)) / Path("../..")))

from nlpsim_methods.methods import *
from nlpsim_utils.utilities import *
from nlpsim_utils.helper import *
from nlpsim_utils.nlp_logging import *
from nlpsim_main.params import *
from nlpsim_main.process_args import *


# nltk.download("stopwords")
# nltk.download('punkt')


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


class Input:
    def __init__(self, actual_answer=None, utterance_answer=None,
                 correct_ans_variances=None, other_options=None, threshold=0.0, method='None'):
        self.actual_answer = actual_answer
        self.utterance_answer = utterance_answer
        self.correct_ans_variances = correct_ans_variances
        self.other_options = other_options
        self.threshold = threshold
        self.method = method
        pass


class GetSimilarity:
    def __init__(self, cwd=None, threshold=0.4):
        self.config = Params()
        self.utils = Utilities()
        self.methods = Methods(threshold, self.config)
        self.helper = Helper()
        self.logger = LogAppStd(cwd)
        self.argparse = ProcessArgs(cwd, threshold)
        self.output = Result()
        # self.rhyming = GetRhymingWords()
        self.threshold = threshold
        self.enable_rhyming = self.config.enable_rhyme
        self.get_best_match = self.config.get_best_match
        self.best_th = self.config.best_th
        self.use_methods = ['DirectMatch', 'Cosine', 'NumWord', 'SynAnt', 'Partial', 'Rhyme', 'HybridMatch',
                            'WordForm', 'FuzzyMatch', 'OtherOptionsAnswered']
        self.reject_match_methods = ['SynAnt', 'WordForm', 'OtherOptionsAnswered']
        self.logger.log_info('Loaded RunTime Parameters')
        pass

    def use_method(self, args):
        actual_answer, utterance_answer, threshold = args.actual_answer, args.utterance_answer, args.threshold
        # self.nlpsim_methods.match_using_jaccard_similarity(actual_answer, utterance_answer, threshold)
        if args.method == 'OtherOptionsAnswered':
            is_similar, other_option_match_score, matched_utterance = \
                self.methods.check_if_other_options_answered(args)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, other_option_match_score, matched_utterance))
            return Result(match_score=other_option_match_score, match_method=args.method, is_similar=is_similar,
                          match_word=matched_utterance)

        if args.method == 'DirectMatch':
            is_similar, dm_score, matched_utterance = \
                self.methods.is_direct_match(args)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, dm_score, matched_utterance))
            return Result(match_score=dm_score, match_method=args.method, is_similar=is_similar,
                          match_word=matched_utterance)

        elif args.method == 'NumWord':
            is_similar, nw_score, skip_match = self.methods.match_using_numbers_and_words(args)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, nw_score, args.utterance_answer))
            return Result(match_score=nw_score, match_method=args.method, match_word=args.utterance_answer,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'HybridMatch1':
            is_similar, nw_score, match_word, skip_match = self.methods.match_using_hybrid_num_letters(args)
            utt_ans_match = utterance_answer + ' -({})'.format(match_word)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, nw_score, utt_ans_match))
            return Result(match_score=nw_score, match_method=args.method, match_word=utt_ans_match,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'HybridMatch2':
            is_similar, nw_score, skip_match = self.methods.match_using_hybrid_num_letters_alternate_1(args)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, nw_score, args.utterance_answer))
            return Result(match_score=nw_score, match_method=args.method, match_word=args.utterance_answer,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'HybridMatch3':
            is_similar, nw_score, skip_match = self.methods.match_using_hybrid_num_letters_alternate_2(args)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, nw_score, args.utterance_answer))
            return Result(match_score=nw_score, match_method=args.method, match_word=args.utterance_answer,
                          is_similar=is_similar, skip_match=skip_match)

        elif args.method == 'SynAnt':
            check = self.methods.check_if_syn_ant_match(actual_answer, utterance_answer)
            if check and not self.config.reject_syn_ant_match:
                check = False
            self.logger.log_info('Method: {} - isSynAnt: {} - RejectParam: {}'
                                 .format(args.method, check, self.config.reject_syn_ant_match))
            return Result(match_method=args.method, skip_match=check, match_word=args.utterance_answer)

        elif args.method == 'WordForm':
            check = self.methods.check_if_word_forms_match(actual_answer, utterance_answer)
            if check and not self.config.reject_word_forms:
                check = False
            self.logger.log_info('Method: {} - isWordForm: {} - RejectParam: {}'.
                                 format(args.method, check, self.config.reject_word_forms))
            return Result(match_method=args.method, skip_match=check, match_word=args.utterance_answer)

        elif args.method == 'Cosine':
            is_similar, cosine_score = \
                self.methods.match_using_cosine_similarity(actual_answer, utterance_answer, threshold)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, cosine_score, utterance_answer))
            return Result(match_score=cosine_score, match_method=args.method, is_similar=is_similar,
                          match_word=utterance_answer)

        elif args.method == 'Partial':
            is_similar, ov_score, overlap_word = \
                self.methods.match_using_string_overlap(actual_answer, utterance_answer, threshold)
            utt_ans_overlap = utterance_answer + ' -({})'.format(overlap_word)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, ov_score, overlap_word))
            return Result(match_score=ov_score, match_method=args.method,
                          is_similar=is_similar, match_word=utt_ans_overlap)

        elif args.method == 'Rhyme':
            is_similar, rh_score, rhyme_word = \
                self.methods.match_using_rhyming_words(actual_answer, utterance_answer, threshold, best_match=False)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, rh_score, rhyme_word))
            return Result(match_score=rh_score, match_method=args.method,
                          is_similar=is_similar, match_word=rhyme_word)

        elif args.method == 'FuzzyMatch':
            is_similar, fm_score, fm_word = \
                self.methods.match_using_fuzzy_logic(actual_answer, utterance_answer)
            self.logger.log_info('Method: {} - Similar: {} - Score: {} - Matched {}'.
                                 format(args.method, is_similar, fm_score, fm_word))
            return Result(match_score=fm_score, match_method=args.method,
                          is_similar=is_similar, match_word=fm_word)
        else:
            self.logger.log_error('Method {} is not supported'.format(args.method))
        return Result(processed=False)

    def find_similarity(self, args):
        score, utt_ans, method = [], [], []

        args.threshold = self.threshold
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

        args.method = 'HybridMatch1'
        hybrid_match_result = self.use_method(args)
        score.append(hybrid_match_result.score), utt_ans.append(hybrid_match_result.match_word)
        method.append(hybrid_match_result.match_method)
        if hybrid_match_result.is_similar or hybrid_match_result.skip_match:
            return hybrid_match_result

        args.method = 'HybridMatch2'
        args.threshold = self.config.hybrid_match_alternate_threshold
        hybrid_match_alternate_result = self.use_method(args)
        score.append(hybrid_match_alternate_result.score), utt_ans.append(hybrid_match_alternate_result.match_word)
        method.append(hybrid_match_alternate_result.match_method)
        if hybrid_match_alternate_result.is_similar or hybrid_match_alternate_result.skip_match:
            return hybrid_match_alternate_result

        args.method = 'HybridMatch3'
        args.threshold = self.config.hybrid_match_alternate_threshold
        hybrid_match_alternate_result = self.use_method(args)
        score.append(hybrid_match_alternate_result.score), utt_ans.append(hybrid_match_alternate_result.match_word)
        method.append(hybrid_match_alternate_result.match_method)
        if hybrid_match_alternate_result.is_similar or hybrid_match_alternate_result.skip_match:
            return hybrid_match_alternate_result

        args.threshold = self.threshold
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

        args.threshold = self.threshold
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

    @staticmethod
    def populate_payload(args, match_result):
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
                return self.populate_payload(raw_args, self.output)
            scores_list, word_list, method_list, similar_list = [], [], [], []
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
                    for u_sentence in filtered_args.utterance_answer:
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
                return self.populate_payload(processed_args, Result(match_method='Value Error Exception'))
            except BaseException as e:
                self.logger.log_error('Got ERROR ' + str(e))
                return self.populate_payload(processed_args, Result(match_method='Got ERROR ' + str(e)))
            except:
                self.logger.log_error('Got Unknown Exception')
                return self.populate_payload(processed_args, Result(match_method='Got Unknown Exception'))
        except:
            self.logger.log_error('Got Unknown Exception')
            return self.populate_payload(Input(), Result(match_method='Got Unknown Exception'))

    def process(self, **kwargs):
        return self.get_similarity(**kwargs)


if __name__ == '__main__':
    print('Similarity Function Called: Done')
