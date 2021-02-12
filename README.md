# nlp_similarity
nlp based similarity of utterances

nlp similarity of two utterances can be computed by using below two methods:
1. Using API call:
  from nlpsim_api import *
  
2. Using offline method:
            
        from nlpsim_main.similarity import GetSimilarity
        
        sentence_pairs += [["P v narsimharao", "[pv narsimha rao, pvnarsmhra]"]]
        
        get_similarity = GetSimilarity(threshold=0.4)
        
        for pair in sentence_pairs:
          if len(pair) == 4:
              match = get_similarity.process(
                  s1=pair[0], s2=pair[1],s3=pair[2],s4=pair[3], th=threshold)
          elif len(pair) == 3:
              match = get_similarity.process(
                  s1=pair[0], s2=pair[1],s3=pair[2], th=threshold)
          else:
              match = get_similarity.process(s1=pair[0], s2=pair[1], th=threshold)
              
          print('s2 = {}'.format(match.entered_ans))
          print('s3 = {}'.format(match.true_alternatives))
          print('s4 = {}'.format(match.other_options))

          print("Similar = {0} , with Score = {1:.3f}%, Match Word : '{2}', From Method : '{3}'\n".format(
              match.is_similar, match.score, match.match_word, match.match_method))
  
