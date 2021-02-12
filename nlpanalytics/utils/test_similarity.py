#!/usr/bin/python
import os
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/nlp/nlp_similarity/src')
import src
from src.similarity import *

if __name__ == '__main__':

    threshold = 0.4
    get_similarity = GetSimilarity(threshold=threshold)
    # test data for testing
    sentence_pairs = [["Predator", "[register, ragister, Raja Theatre, rajada, projector, Rajinder, Raja beta, "
                                   "editor, Rajat, Raja Tata]"],
                     ['"False"','["true","through","crew","kru","ru","Churu","cru","Rooh","fru","shrew"]']]
    sentence_pairs += [['"12"', '["20 lacs","20 likes","20 lakes","twenty lacs","20 legs","26","twenty lakes",'
                                '"20 lights","XX lakes","20 lax"]'],
                       ['"Wind"','["what wind","what is wind","what weed","what are wind","what did","what we need",'
                                 '"what Veedu","what we did","wot wind","wart wind"]'],
                       ['"defend"', '["depend", "defende", "defend", "defined", "Defender", "defendant", '
                                    '"dependent", "different", "defended", "defend it"]'],
                       ['355', 'three fifty five'], ['1234', 'one thousand two hundred thirty four'],
                       ['enforce', 'manforce'], ['ram naresh', 'am mahesh'], ['twenty nine', '29'],['Frog', 'Frogs'], ['enforce', 'force'], ['enforce', 'horse'], ['male', 'female'],
                      ['Angrier', 'angry'], ['108', 'one hundred eight'],
                      ['1234', 'one thousand two hundred thirty four'],
                      ['"Precipitation"', '["evaporation","pervaporation"]']]

    sentence_pairs += [['"Deewana"', '["gana","gaana","Aana","Rana","Nana","na","banana","Jana","Ghana"]'],
                       ['"7"', '"7 bar"'], ['"potato"', '["tomato"]'],
                       ['"Dilli Haat"', '["दिल्ली हाट","दिल्ली आर्ट","दिल्ली 8","दिल्ली हट","दिल्ली आज",'
                                        '"दिल्ली आठ","दिल्ली हेड","दिल्ली अट"]'],
                      ['"3"', '["42","42 le","photo editor","forty two","43","40 trailer","442","42a","42mm","40/2"]'],
                      ['"Nagaland"', '["नागालैंड","नागा लैंड"]'], ['"क्रिसमस"', '["कृष्ण","क्रिसमस","कृष्णा"]'],
                      ['"सही है"', '["सही","कहीं","शशि","शशी","सच्ची","कही","कल की","सकी","सखी"]'],
                      ['"Dr. B.R. Ambedkar"', '["Dr BR Ambedkar","Dr B R Ambedkar","daw bi R Ambedkar",'
                                              '"Doctor BR Ambedkar","doctor bi R Ambedkar","doctor B R Ambedkar",'
                                              '"daw BR Ambedkar","D R B R Ambedkar","Dr b.r. Ambedkar"]'],
                      ['"Male"', '"Female"'],
                      ['"Fragile"','["resign","present","design","president","join","result","jail","rejoin","Brazil"]'],
                      ['"3"', '["42","42 le","photo editor","forty two","43","40 trailer","442","42a","42mm","40/2"]']]
    sentence_pairs += [['"Indefinite"', '["definite","definitely","definition"]']]
    sentence_pairs += [['"defend"' ,'["depend", "defende", "defend", "defined", "Defender", "defendant", "dependent", '
                                   '"different", "defended", "defend it"]']]
    sentence_pairs += [['"Lychee"',
                        '["lichi","lici","litchi","leechi","lichy","leaching","leacy","litchy","leeching", "Richie"]']]
    sentence_pairs += [['"one thousand and eight hundred and thirty"', '["1830"]'],
                      ['"Male"', '"Female"'], ['"Reversible"', 'Irreversible'],
                      ['"Fragile"',
                       '["resign","present","design","president","join","result","jail","rejoin","Brazil"]'],
                      ['"Maple"', '["nipple", "nipal","neeple","nipl","nippl", "nippel", "Neet Pal", "nipel", "Ne Pal", "nippple"]'],
                      ['"nizaumuddin dargah"', '["nizamuddin dargah"]'],
                      ['"Lychee"',
                       '["lichi","lici","litchi","leechi","lichy","leaching","leacy","litchy","leeching", "Richie"]',
                       '["lichy", "lichi"]'],
                      ["15 meter", "[five meter, 14 meter, 15meter, fifteen meter]",' ',"[25 meter, 35 meter, 45 meter]"],
                      ["Hinge Joints", "[pivot joint, pivot joints, rivet joint, favourite joint, David joint, fitjoint]"],
                      ["Hinge Joints",
                       "[pivot joint, pivot joints, rivet joint, favourite joint, David joint, fitjoint]", '',
                       "[pivot joints, rivet joints, plane joints]"],
                      ["Hinge Joints",
                       "[pivot joint, pivot joints, rivet joint, favourite joint, David joint, fitjoint, hingejoints]", '',
                       "[pivot joints, rivet joints, plane joints]"],
                      ["correct", "[incorrect]"],
                      ["Relative pronoun", "[pronoun]", '',
                       "[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]"],
                      ["Relative pronoun", "[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]", '',
                       "[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]"],
                      ["Relative pronoun", "[pronoun]"],
                      ["Relative pronoun", "[Reflexive pronoun]"],
                       ["Relative pronoun", "[Reflexive pronoun]", '',
                       "[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]"]]
    sentence_pairs += [["au revoir", "[arever, a river, auvier, a reservior, aurevoir]"],
                      ["वडील", "[भाउु, तू बाोलताोस, मुलगा, वडीभाउुल, तूवडील]"]]
    sentence_pairs = [["Modify Verbs Adjectives Adverbs ", "[Modify Verbs and Adjectives and Adverbs]", '',
                       "[Modify Verbs, Modify Verbs and Adjectives, Remove Unwanted Information]"]]
    sentence_pairs += [["Modify Verbs Adjectives Adverbs ", "[Modify Verbs and Adjectives]", '',
                        "[Modify Verbs, Modify Verbs and Adjectives, Remove Unwanted Information]"]]
    sentence_pairs += [["Modify Verbs Adjectives Adverbs ", "[Modified Verbs, Modified verb]", '',
                        "[Modify Verbs, Modify Verbs and Adjectives, Remove Unwanted Information]"]]
    sentence_pairs += [["Modify Verbs and Adjectives ", "[Modify Verbs and Adjectives and Adverbs]", '',
                        "[Modify Verbs, Modify Verbs and Adjectives and Adverbs, Remove Unwanted Information]"]]
    sentence_pairs += [["sita rammohan", "[mohanram]", '',
                        "[ram, sita ram, sita ram mohan agarwal]"]]
    sentence_pairs += [["Diagon Alley", "[black Alley","black Allah","black Ali","black Kale","black allergy","black colour","black Gale","black","black wale","black Kali]"]]
    sentence_pairs = [["Honesty", "[best, west]"]]
    #    get_similarity = GetSimilarity(threshold=0.4)
    for pair in sentence_pairs:
        if len(pair) == 4:
            match = get_similarity.process(
                s1=pair[0], s2=pair[1],s3=pair[2],s4=pair[3], th=threshold)
        elif len(pair) == 3:
            match = get_similarity.process(
                s1=pair[0], s2=pair[1],s3=pair[2], th=threshold)
        else:
            match = get_similarity.process(s1=pair[0], s2=pair[1], th=threshold)
        #
        #print("Correct Answer = {}".format(pair[0]))
        #print("Entered = {}".format(pair[1]))
        print('s1 = {}'.format(match.actual_answer))
        print('s2 = {}'.format(match.entered_ans))
        print('s3 = {}'.format(match.true_alternatives))
        print('s4 = {}'.format(match.other_options))

        print("Similar = {0} , with Score = {1:.3f}%, Match Word : '{2}', From Method : '{3}'\n".format(
            match.is_similar, match.score, match.match_word, match.match_method))
# #       curl localhost: 5000 / post - i'{"correct answer is 1947"} - e {"1947 sorry oh yes 1947"}'
#localhost:5000/similarity?s1="Relative pronoun"&s2="[pronoun]"&s3=''&s4="[Indefinite pronoun, Distributive pronoun, Reflexive pronoun]"