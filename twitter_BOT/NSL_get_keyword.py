from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

DEFAULT_RELEVANCE_TOLERANCE = 0.5

def NSL_get_keyword( txt ):

    # Create the AlchemyAPI Object
    alchemyapi = AlchemyAPI()
    result = []

    print('Processing text: ', txt)

    # get response
    response = alchemyapi.keywords('text', txt, {'sentiment': 1})

    if response['status'] == 'OK':
        
        # print('## Response Object ##')
        # print(json.dumps(response, indent=4))
        # print('')
        
        print('## Keywords ##')
        for keyword in response['keywords']:
            txt = keyword['text'].encode('utf-8')
            relevance = keyword['relevance']
            sentiment = keyword['sentiment']['type']
            score = 0
            if 'score' in keyword['sentiment']:
                score = keyword['sentiment']['score']
            
            print('     text: ', txt )
            print('     relevance: ', relevance )
            print('     sentiment: ', sentiment )
            print('     sentiment score: ' + str(score) )
            
            print('')
            if relevance > DEFAULT_RELEVANCE_TOLERANCE:
                result.append( txt )
            
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
        
    return result
    
    
def main():
    txt = "@onetoday what i can do for the africa? i want to be a hero! find me a project"
    rsp = NSL_get_keyword( txt )
    print( rsp )
    
if __name__ == '__main__':
  main()
  