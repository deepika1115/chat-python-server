#!/usr/bin/env python

import cgi
import webapp2
import json
import urllib2
import logging
from firebase import Firebase
# config = {
#     "apiKey": "AIzaSyBYFpiIPeBz69p0CSJ92I3iC218t3yiQgk",
#     "authDomain": "chat-interface1.Firebaseapp.com",
#     "databaseURL": "https://chat-interface1.Firebaseio.com",
#     "storageBucket": "chat-interface1.appspot.com",
#     "serviceAccount": "path/to/serviceAccountCredentials.json"
# }
# Firebase = pyrebase.initialize_app(config)

class MainPage(webapp2.RequestHandler):
    
    def post(self):
        self.response.headers['Content-type'] = 'application/json'
        
        logging.info(json.loads(self.request.body))
        data = json.loads(self.request.body)['result']['resolvedQuery']
        session_id = json.loads(self.request.body)['sessionId']
        obj = {
        "text": '*SESSION ID:* ' + session_id +' ' + data

        }

        req = urllib2.Request('https://hooks.slack.com/services/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')
        req.add_header('Content-Type', 'application/json')
        
        ob = {
        "speech": "sending to slack",
        "displayText": "sending to slack",
        "data": {},
        "contextOut": [],
        "source": "Deepika"
        }
        self.response.out.write(json.dumps(ob))
        response = urllib2.urlopen(req, json.dumps(obj))

class RespPage(webapp2.RequestHandler):

   
    def post(self):
        logging.info(self.request.body)
        slack_data = dict(x.split('=') for x in self.request.body.split('&'))
        txdata = slack_data['text'].replace("+"," ")
        rdata = txdata.split('%3A')
        session_id = rdata[0]
        msg = rdata[1]

        logging.info(slack_data)
        f = Firebase('https://chat-interface1.Firebaseio.com/chat-interface1')
        # r = f.push({'session_id': session_id, 'message': msg})
        # c = f.child(session_id)
        f.push({'session_id': session_id, 'message': msg})
        
        # result = Firebase.post('/messages', txdata, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
    def get(self):
        self.response.out.write('2 mins, running')
        
        
app = webapp2.WSGIApplication([
  ('/no', MainPage),
  ('/res',RespPage)
], debug=True)