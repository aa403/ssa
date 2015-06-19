__author__ = 'sslr'

import json

from flask import Flask
from flask import request
from flask import jsonify

from flask import Response

from src.main.handlers.manage_sentiment import manage_sentiment_analysis as run_sentiment_analysis
from src.main.algorithms.sentiment_wordnet import SentimentWordnet
from src.main.nlp_core.annotation import Annotator

app = Flask(__name__)
wordnet = SentimentWordnet()
annotator = Annotator()

class APIException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def decode_request(request_obj):

    if request.headers['Content-Type'] != 'application/json':
        raise APIException("Content-type needs to be application/json.", 405)
    request_dict = json.loads(request_obj.data)
    return request_dict

def validate_request(request_obj):

    message = 'An error occurred: '

    if request_obj['data'] is None:
        message += "Field 'data' wasn't provided in the request."
        print 'Raising exception: ' + message
        raise APIException(message, 400)

    if type(request_obj['data']) is not list:
        message += "Field 'data' is not a list of strings."
        print 'Raising exception: ' + message
        raise APIException(message, 400)

    if not request_obj['data']:
        message += "Field 'data' is not present."
        print 'Raising exception: ' + message
        raise APIException(message, 400)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment_analysis():

    request_obj = decode_request(request)
    validate_request(request_obj)

    result = run_sentiment_analysis(annotator, wordnet, request_obj['data'])

    converted_result = {key: value.to_dict() for key, value in result.iteritems()}

    js = json.dumps(converted_result)

    return Response(js, status=200, mimetype='application/json')


if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
