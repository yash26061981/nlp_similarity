#!/usr/bin/python
# -*- coding: utf-8 -*-
import pronouncing
from Phyme import Phyme
import numpy as np


class GetRhymingWords:

    def __init__(self, pronounce=True, phyme=True):
        self.use_pronounce = pronounce
        self.use_phyme = phyme
        if not self.use_pronounce and not self.use_phyme:
            self.use_pronounce = True
        self.phyme = Phyme()
        self.pronounce = pronouncing
        self.get_perfect_rhymes = True
        self.get_family_rhymes = False
        self.get_partner_rhymes = False
        self.get_additive_rhymes = False
        self.get_subtractive_rhymes = False
        self.get_substitution_rhymes = False
        self.get_assonance_rhymes = False
        self.get_consonant_rhymes = False
        pass

    def get_words_from_pronounce(self, word):
        matching_words = self.pronounce.rhymes(word)
        return matching_words

    def remove_noise(self, word_list):
        f_word = [w.split('(')[0] for w in word_list]
        f1_word = [w.lower() for w in f_word]
        return f1_word

    def parse_rhyme_from_dict(self, dict_words):
        values = list()
        for key, value in dict_words.items():
            values += value
        values = np.unique(values)
        return self.remove_noise(values)

    def get_rhyme_words_mode(self, word, mode):
        if mode == 'perfect':
            func = self.phyme.get_perfect_rhymes
        elif mode == 'family':
            func = self.phyme.get_family_rhymes
        elif mode == 'partner':
            func = self.phyme.get_partner_rhymes
        elif mode == 'additive':
            func = self.phyme.get_additive_rhymes
        elif mode == 'subtractive':
            func = self.phyme.get_subtractive_rhymes
        elif mode == 'substitution':
            func = self.phyme.get_substitution_rhymes
        elif mode == 'assonance':
            func = self.phyme.get_assonance_rhymes
        elif mode == 'consonant':
            func = self.phyme.get_consonant_rhymes
        else:
            print('Undefined Mode')

        try:
            rhyming_word = func(word)
            return rhyming_word
        except KeyError as e:
            #print('I got a KeyError - reason "%s"' % str(e))
            return None
        except IndexError as e:
            #print('I got an IndexError - reason "%s"' % str(e))
            return None

    def get_words_from_phyme(self, word):
        matching_words = list()

        # perfect rhymes
        if self.get_perfect_rhymes:
            perfect_rhymes = self.get_rhyme_words_mode(word, 'perfect')
            if perfect_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(perfect_rhymes)

        # find rhymes with the same vowels and consonants of the same type (fricative, plosive, etc) and voicing
        # (voiced or unvoiced). FOB -> DOG
        if self.get_family_rhymes:
            family_rhymes = self.get_rhyme_words_mode(word, 'family')
            if family_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(family_rhymes)

        # find rhymes with the same vowels and consonants of the same type, regardless of voicing. HAWK -> DOG
        if self.get_partner_rhymes:
            partner_rhymes = self.get_rhyme_words_mode(word, 'partner')
            if partner_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(partner_rhymes)

        # find rhymes with the same vowels and consonants, as well as any extra consonants. DUDES -> DUES
        if self.get_additive_rhymes:
            additive_rhymes = self.get_rhyme_words_mode(word, 'additive')
            if additive_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(additive_rhymes)

        # find rhymes with the same vowels and a subset of the same consonants. DUDE -> DO
        if self.get_subtractive_rhymes:
            subtractive_rhymes = self.get_rhyme_words_mode(word, 'subtractive')
            if subtractive_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(subtractive_rhymes)

        # find rhymes with the same vowels and some of the same consonants, with some swapped out for other consonants.
        # FACTOR -> FASTER
        if self.get_substitution_rhymes:
            substitution_rhymes = self.get_rhyme_words_mode(word, 'substitution')
            if substitution_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(substitution_rhymes)

        # find rhymes with the same vowels and arbitrary consonants. CASH -> CATS
        if self.get_assonance_rhymes:
            assonance_rhymes = self.get_rhyme_words_mode(word, 'assonance')
            if assonance_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(assonance_rhymes)

        # find word that do not have the same vowels, but have the same consonants. CAT -> BOT
        if self.get_consonant_rhymes:
            consonant_rhymes = self.get_rhyme_words_mode(word, 'consonant')
            if consonant_rhymes is not None:
                matching_words += self.parse_rhyme_from_dict(consonant_rhymes)

        return np.unique(matching_words).tolist()

    def suggest(self, word, apply_rules=True, offset=2):
        matching_words1, matching_words2 = [], []
        if self.use_pronounce:
            matching_words1 = self.get_words_from_pronounce(word)
        if self.use_phyme:
            matching_words2 = self.get_words_from_phyme(word)
        matching_words = np.unique(matching_words1 + matching_words2)
        if matching_words is None:
            return matching_words
        if apply_rules:
            word_len = len(word)
            processed_words = [word.replace(".", "") for word in matching_words]
            suggested_len = [len(mw) for mw in processed_words]
            match_index = [index for index, value in enumerate(suggested_len) if abs(word_len - value) <= offset]
            suggested_words = [processed_words[i] for i in match_index]
            return suggested_words
        return matching_words

    def check_if_rhyming(self, a_ans, u_ans):
        a_ans_rhyming = self.suggest(a_ans, apply_rules=False)
        u_ans_rhyming = self.suggest(u_ans, apply_rules=False)
        if a_ans in u_ans_rhyming or u_ans in a_ans_rhyming:
            return True
        return False


if __name__ == '__main__':
    rhyming_words = GetRhymingWords(pronounce=True, phyme=True)
    search_word = 'relative'#'Lychee'
    words = rhyming_words.suggest(search_word, apply_rules=True, offset=2)
    print('Rhyming words of "{0}" are -> {1}' .format(search_word.upper(), words))
    if words is not None:
        print('Total Findings : ', len(words))
