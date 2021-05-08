from flask import jsonify
from flask import Flask
from flask import request
from flask import Response
from flask import make_response
from flask_cors import CORS, cross_origin
import nlpIO

NLP = nlpIO.NLPUnit()
app = Flask(__name__)
cors = CORS(app)
@app.after_request
def after_request(response):

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response


@app.route('/process', methods=['GET', 'POST', 'OPTIONS'])
def process (param=None, pid=None):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    if param == None:
        data = request.get_json()
        data = NLP.processRequest(data)
        resp = Response(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        free_text = param
        resp = Response(NLP.processText(free_text, pid))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/query', methods=['GET', 'POST', 'OPTIONS'])
def query( text=None):
    if text == None:
        data = request.get_json()
        data = NLP.processQuery(data)
        return data
    
@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def home():
    return """<html>
          <head>
            
          </head>
          <body>
          <h1>medaCy Free Text Entry</h1>
            <form method="post" action="process">
              <input type="text" value="50" name="param"/>
              <input type="text" value="5" name="pid"/>
              <button type="submit">Submit</button>
            </form>
          </body>
        </html>"""

@app.route('/assisted-query', methods = ['GET', 'POST', 'OPTIONS'])
def assisted():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        data = request.get_json()
        query = data['NLQuery']
        #try ln2sql query
        try:
            sqltry = NLP.processNLQuery(data)
            return jsonify(sqltry)
        except:
            return {"Data": "NONE"}
##        resp = Response(sqltry)
##        resp.headers['Access-Control-Allow-Origin'] = '*'
##        return resp

@app.route('/add-patient', methods = ['GET', 'POST', 'OPTIONS'])
def add_patient():
     if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
     else:
         data = request.get_json()
         success = NLP.insertPatient(data)
         
         return jsonify(success)
     


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080, debug = True, threaded = True)
