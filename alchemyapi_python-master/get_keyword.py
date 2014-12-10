from __future__ import print_function
from alchemyapi import AlchemyAPI
import json


demo_text = 'Yesterday dumb Bob destroyed my fancy iPhone in beautiful Denver, Colorado. I guess I will have to head over to the Apple Store and buy a new one.'
demo_url = 'http://www.npr.org/2013/11/26/247336038/dont-stuff-the-turkey-and-other-tips-from-americas-test-kitchen'
demo_html = '<html><head><title>Python Demo | AlchemyAPI</title></head><body><h1>Did you know that AlchemyAPI works on HTML?</h1><p>Well, you do now.</p></body></html>'
image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'


# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()


# response = alchemyapi.keywords('text', demo_text, {'sentiment': 1})

txt = "@onetoday, what i can do for the children in africa? i want to be a hero! so, provide me a project."
response = alchemyapi.keywords('text', txt, {'sentiment': 1})

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')
    print('## Keywords ##')
    for keyword in response['keywords']:
        print('text: ', keyword['text'].encode('utf-8'))
        print('relevance: ', keyword['relevance'])
        print('sentiment: ', keyword['sentiment']['type'])
        if 'score' in keyword['sentiment']:
            print('sentiment score: ' + keyword['sentiment']['score'])
        print('')
else:
    print('Error in keyword extaction call: ', response['statusInfo'])