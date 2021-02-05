import requests
import json

def test_similarity():
    sentence_pairs = [["I love horror movies", "Lights out is a horror movie"],
                      ["correct answer is 1947", "i think answer is 1947 sorry no yes answer is 1947"],
                      ["correct answer is 1947", "i think answer is 1948 sorry no yes yes yes answer is 1947"],
                      ["correct answer is 1947", "i think answer is 1948 sorry no yes answer is 1948"],
                      ["1947", "1948 sorry 1947"],
                      ["correct answer is 1947", "1947 sorry oh yes 1947"],
                      ["correct answer is 1947", "1950 sorry 1947"],
                      ["we have to multiply it by 2", "it has to be multiple of 2"],
                      ["pandit jawahar lal nehru", "jawahar nehru"],
                      ["pandit jawahar lal nehru", "i think the answer is pandit jawahar lal nehru hmm urrr"],
                      ["double trouble bubble", "bubble"],
                      ["If I don't buy some new music every month I get bored with my collection",
                       "I get bored with my collection so I buy some new music every month"]]

    for pair in sentence_pairs:
        pass_url = 'http://localhost:5000/similarity?s1="{0:}"&s2="{1:}"'.format(pair[0], pair[1])
        receive = requests.get(pass_url)
        # print(receive.content)
        txt = receive.text.split(',')
        print(txt[0].split('{')[1])
        print(txt[1])
        score = float(txt[2].split(':')[1])
        simi = txt[3].split(':')[1]
        tms = float(txt[4].split('}')[0].split(':')[1])
        print("Score = {0:.2f},  Similarity = {1},  Time in milliseconds = {2:.4f}\n".format(score, simi, (tms * 1000)))


def test_rhyming_words():
    word = 'rice'
    rule = 'true' # true / false
    offset = 2 # 0 <= o <=3
    pass_url = 'http://localhost:5000/rhyme?w={0:}&r={1:}&o={2:}'.format(word, rule, offset)
    receive = requests.get(pass_url)
    #print(receive.text)
    js = json.loads(receive.text)
    print('Original_Word : ', js['Original_Word'])
    print('Rhyming_Words : ', js['Rhyming_Words'])
    print('Time (ms) : {:.4f} '.format(js['Time in seconds']*1000))
    print('Total Words : ', js['Total Words'])


def search_character_level(cs, ss):
    if len(cs) == len(ss):
        return 0



def test():
    #test_rhyming_words()
    #test_similarity()
    from re import search
    fs = 'Narendra Damodar Das Modi'.lower()
    ss = 'Modi Ji'.lower()
    print(search(ss, fs))

    import inflect

    p = inflect.engine()

    cat_count = 1
    print("I saw", cat_count, p.plural("cat", cat_count))

    word = 'frog'
    is_singular = False
    plural_w = word
    singular_w = p.singular_noun(word)
    if not singular_w:
        is_singular = True
    if is_singular:
        singular_w = word
        plural_w = p.plural(word)
    print('Word : ', word, ' Singular Word is: ', singular_w, ' Plural Word is : ', plural_w)
    word = 'in'
    is_singular = False
    plural_w = word
    singular_w = p.singular_noun(word)
    if not singular_w:
        is_singular = True
    if is_singular:
        singular_w = word
        plural_w = p.plural(word)
    print('Word : ', word, ' Singular Word is: ', singular_w, ' Plural Word is : ', plural_w)


    print(p.singular_noun("they"))  # 'it'
    print(p.singular_noun("they"))  # 'she'
    print(p.number_to_words(1234))
    # "one thousand, two hundred and thirty-four"
    print(p.number_to_words(p.ordinal(1234)))
    # "one thousand, two hundred and thirty-fourth"

    # GET BACK A LIST OF STRINGS, ONE FOR EACH "CHUNK"...

    print(p.number_to_words(1234, wantlist=True))
    # ("one thousand","two hundred and thirty-four")

    # OPTIONAL PARAMETERS CHANGE TRANSLATION:

    print(p.number_to_words(12345, group=1))
    # "one, two, three, four, five"

    print(p.number_to_words(12345, group=2))
    # "twelve, thirty-four, five"

    print(p.number_to_words(12345, group=3))
    # "one twenty-three, forty-five"

    print(p.number_to_words(1234, andword=""))
    # "one thousand, two hundred thirty-four"

    print(p.number_to_words(1234, andword=", plus"))
    # "one thousand, two hundred, plus thirty-four"
    # TODO: I get no comma before plus: check perl

    print(p.number_to_words(555_1202, group=1, zero="oh"))
    # "five, five, five, one, two, oh, two"

    print(p.number_to_words(555_1202, group=1, one="unity"))
    # "five, five, five, unity, two, oh, two"

    print(p.number_to_words(123.456, group=1, decimal="mark"))
    # "one two three mark four five six"
    # TODO: DOCBUG: perl gives commas here as do I

    num = '1234'
    numstr = p.number_to_words(num)
    #numstr.replace("","")
    print(numstr.replace(",","").replace("-"," "))
    print(num.isdigit())
    from word2number import w2n

    print(w2n.word_to_num('twelve'))


if __name__ == '__main__':
    print('done')
    from cdifflib import CSequenceMatcher
    import difflib

    s = CSequenceMatcher(lambda x: x == " ","correct answer is 1947", "correct answer is 1948 oh sorry 1950")
    print(round(s.ratio(), 3))
    s = CSequenceMatcher(lambda x: x == " ", "enforce", "time")
    print(round(s.ratio(), 3))

    import difflib
    def get_overlap(s1, s2):
        s = difflib.SequenceMatcher(None, s1, s2)
        pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2))
        return s1[pos_a:pos_a + size]

    print(get_overlap("enforce", "horse"))

