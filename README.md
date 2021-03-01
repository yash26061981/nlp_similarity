# nlp_similarity
nlp based similarity of utterances

nlp similarity of two utterances can be computed by using below two methods:
1. Using API call:
    
    1.1 First Run the API:

        from nlpsim.nlpsim_api import *
        
        if __name__ == '__main__':
            print('Calling API')
            initialise(os.path.dirname(os.path.realpath(__file__)))
            port = int(os.environ.get('PORT', 5000))
            app.run(host='127.0.0.1', port=port, debug=False)
 
    1.2 Call API for nlp similarity:
    
        from nlpsim_api import *

        if __name__ == '__main__':
            s1 = 'worse'
            s2 = '[was, worst, vs, vas, verse, worse, vaaste, watch, bus]'
            s3 = None
            s4 = '[Badest, Worst, Badder]'
            
            reqs = 'http://localhost:5000/similarity?s1={}&s2=[{}]&s3=[{}]&s4=[{}]'.format(s1,s2,s3,s4)
            response = requests.get(reqs)
            print('{}'.format(response.text))

                
2. Using offline method:
            
        from nlpsim_main import *

        if __name__ == '__main__':
            threshold = 0.4
            get_similarity = GetSimilarity(threshold=threshold)
            # test data for testing
            s1 = 'worse'
            s2 = '[was, worst, vs, vas, verse, worse, vaaste, watch, bus]'
            s3 = None
            s4 = '[Badest, Worst, Badder]'
        
            match = get_similarity.process(s1=s1, s2=s2, s3=s3, s4=s4, th=threshold)
            print('s1 = {}'.format(match.actual_answer))
            print('s2 = {}'.format(match.entered_ans))
            print('s3 = {}'.format(match.true_alternatives))
            print('s4 = {}'.format(match.other_options))
        
            print("Similar = {0} , with Score = {1:.3f}%, Match Word : '{2}', From Method : '{3}'\n".format(
                match.is_similar, match.score, match.match_word, match.match_method))
          
