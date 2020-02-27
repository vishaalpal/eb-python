import logging
import logging.handlers

from wsgiref.simple_server import make_server


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/opt/python/log/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>HelpDesk Tips n Tricks</title>
  <style>

  body {
    color: #FFFACD;
    background-color: #A52A2A;
    font-family: Calibri;
    font-size: 15px;
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
     text-shadow: none;
  }
  
  title {
     color: #FFFACD;
  }

  a {
    color: #FFFACD;
  }

  </style>

</head>
<body id="sample">
  <div class="title">
    <h1>Welcome to HelpDesk Tips n Tricks</h1>
    <p>This Python Application has been deployed via AWS Elastic Beanstalk. Any code changes are built and deployed automatically via CI/CD process using Jenkins behind Nginx.</p>
  </div>
  
  <div class="linksColumn"> 
    <h2>About Me</h2>
    <li><a href="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTQhKNVHb7GwZEa7wjVqdSJMqtWiRWW2mw_8xKWT2mpZEJqksng">Here is a picture of Chriz</a>
    <li><a href="https://c402277.ssl.cf1.rackcdn.com/photos/18330/images/hero_small/Mountain_Gorilla_Silverback_WW22557.jpg?1576515753">Here is a picture of Shane</a>
    <li><a href="https://edge.alluremedia.com.au/m/l/2017/10/Qantas.png">Here is a picture of Brandon</a>
    <li><a href="https://www.abc.net.au/news/image/11791604-1x1-940x940.jpg">Here is a picture of Lex</a>
    <li><a href="https://vishaalpal.github.io/">Check out my GitHub profile here</a>
    </li>
  </div>
</body>
</html>
"""

def application(environ, start_response):
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size).decode()
                logger.info("Received message: %s" % request_body)
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ['HTTP_X_AWS_SQSD_TASKNAME'], environ['HTTP_X_AWS_SQSD_SCHEDULED_AT'])
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)
    return [response]


if __name__ == '__main__':
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()
