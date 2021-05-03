#!/usr/bin/python

class Word2Num:
    def __init__(self):
        pass

    @staticmethod
    def is_number(x):
        if type(x) == str:
            x = x.replace(',', '')
        try:
            float(x)
        except:
            return False
        return True

    def word2number(self, word_num, num_words=None):
        if num_words is None:
            num_words = {}
        units = [
            'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
            'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
            'sixteen', 'seventeen', 'eighteen', 'nineteen',
        ]
        tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        scales = ['hundred', 'thousand', 'million', 'billion', 'trillion']
        ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7,
                         'eighth': 8, 'ninth': 9, 'tenth': 10}
        ordinal_endings = [('ieth', 'y'), ('th', ''), ('ths', ''), ('s', ''), ('by', '/')]

        if not num_words:
            num_words['and'] = (1, 0)
            for idx, word in enumerate(units): num_words[word] = (1, idx)
            for idx, word in enumerate(tens): num_words[word] = (1, idx * 10)
            for idx, word in enumerate(scales): num_words[word] = (10 ** (idx * 3 or 2), 0)

        word_num = word_num.replace('-', ' ').replace('/', ' by ')

        current = result = 0
        curr_string = ''
        on_number = False
        last_unit = False
        last_scale = False

        def is_number_word(x):
            if self.is_number(x):
                return True
            if word in num_words:
                return True
            return False

        def from_number_word(x):
            if self.is_number(x):
                scale = 0
                increment = int(x.replace(',', ''))
                return scale, increment
            return num_words[x]

        for word in word_num.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                on_number = True
                last_unit = False
                last_scale = False
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if (not is_number_word(word)) or (word == 'and' and not last_scale):
                    if on_number:
                        # Flush the current number we are building
                        curr_string += repr(result + current) + " "
                        #print('here 1', curr_string)
                    curr_string += word + " "
                    #print('here 2', curr_string)
                    result = current = 0
                    on_number = False
                    last_unit = False
                    last_scale = False
                else:
                    scale, increment = from_number_word(word)
                    on_number = True

                    if last_unit and (word not in scales):
                        curr_string += repr(result + current)
                        #print('here 3', curr_string)
                        result = current = 0

                    if scale > 1:
                        current = max(1, current)

                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0

                    last_scale = False
                    last_unit = False
                    if word in scales:
                        last_scale = True
                    elif word in units:
                        last_unit = True

        if on_number:
            curr_string += repr(result + current)
            #print('here 4', curr_string)

        return curr_string


if __name__ == '__main__':
    w2n = Word2Num()
    print(w2n.word2number("fourteen ones and nine tenths"))
    print(w2n.word2number("13 by 4"))
    print(w2n.word2number("13/4"))
    print(w2n.word2number("lions gate"))
