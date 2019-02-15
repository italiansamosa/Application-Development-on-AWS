from flask import Flask
from flask import request
from urllib2 import urlopen
import json
import re
import sys
import boto3

def compute_top_words (url):
    TOP_N = 10
    text = urlopen(url).read()
    histogram = {}

    for word in re.split('\W+', text):
        if not word in histogram:
            histogram[word] = 0
        histogram[word] += 1

    top_words = sorted(histogram.items(), reverse=True, key=(lambda xs: xs[1]))[:TOP_N]
    return json.dumps(top_words)

app = Flask(__name__)

@app.route('/')

def hello_world():
    url = request.args.get('url')
    #begin logic    
    if url == None:
        return "Provide a URL using 'url' query string parameter : http://.../?url=<url>"
    if url != None:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
        table = dynamodb.Table('UW-Week2')
        try:
            table.get_item(
                Key={
                    'URL':url,
                    'Word':compute_top_words(url)
                }
                )
        except:
            pass
        else:    
            table.put_item(
            Item={
            'URL':url,
            'Word':compute_top_words(url)
            }
            )
            return compute_top_words(url)
            print('Put Item succeeded: New item stored into DynamoDB')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
