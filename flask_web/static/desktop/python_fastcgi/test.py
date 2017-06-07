#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cgi import escape
import sys, os
from flup.server.fcgi import WSGIServer
import redis

def app(environ, start_response):
    r_server = redis.Redis("localhost")
    start_response('200 OK', [('Content-Type', 'text/html')])

    
    response_body = 'The request method was %s' % environ['REQUEST_METHOD'] +"<BR>"
    response_body = response_body +'The file request was %s'%environ["SCRIPT_NAME"]+"<BR>"
    return [response_body]



WSGIServer(app).run()


# from cgi import parse_qs, escape
# Returns a dictionary containing lists as values.
#   d = parse_qs(environ['QUERY_STRING'])

# In this idiom you must issue a list containing a default value.
# age = d.get('age', [''])[0] # Returns the first age value.
# hobbies = d.get('hobbies', []) # Returns a list of hobbies.

# Always escape user input to avoid script injection
# age = escape(age)
# hobbies = [escape(hobby) for hobby in hobbies]

# response_body = html % (age or 'Empty',
#               ', '.join(hobbies or ['No Hobbies']))


#from cgi import parse_qs, escape
# the environment variable CONTENT_LENGTH may be empty or missing
#   try:
#      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
#   except (ValueError):
#      request_body_size = 0

   # When the method is POST the query string will be sent
   # in the HTTP request body which is passed by the WSGI server
   # in the file like wsgi.input environment variable.
#   request_body = environ['wsgi.input'].read(request_body_size)
#   d = parse_qs(request_body)

#   age = d.get('age', [''])[0] # Returns the first age value.
#   hobbies = d.get('hobbies', []) # Returns a list of hobbies.

   # Always escape user input to avoid script injection
#   age = escape(age)
#   hobbies = [escape(hobby) for hobby in hobbies]

#   response_body = html % (age or 'Empty',
#               ', '.join(hobbies or ['No Hobbies']))

