
import sys
import os
import logging
import time
import datetime
import json
import uuid
import requests
import ast
from flask import Flask, request , render_template
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
app.debug = True

class OPERATIONS(Resource):
        @app.route('/',methods=['GET'])
        def hello_world():
            return 'Hello World!'

        @app.route('/customerupdate',methods=['GET','POST'])
        def customerupdate():
            print "************DEBUG 1 ***********"
            RequestValues = request.values
            print RequestValues
            print "************DEBUG 2 ***********"
            RequestForm = request.form
            print RequestForm
            print "************DEBUG 2-1 ***********"
            so = RequestForm
            json_of_metadatas = so.to_dict(flat=False)
            print json_of_metadatas
            print "************DEBUG 2-2 ***********"
            MetdatasFromJSON = json_of_metadatas['json']
            print MetdatasFromJSON          
            print "************DEBUG 2-3 ***********"
            MetdatasFromJSON0 = MetdatasFromJSON[0]
            print MetdatasFromJSON0
            print "************DEBUG 3-4 ***********"
            strMetdatasFromJSON0 = str(MetdatasFromJSON0)
            print strMetdatasFromJSON0
            print "************DEBUG 3-4-1 ***********" 
            MetdatasDICT = ast.literal_eval(strMetdatasFromJSON0)
            print MetdatasDICT
            print "************DEBUG 3-5 ***********"
            for key in MetdatasDICT :
                print "key: %s , value: %s" % (key, MetdatasDICT[key])
                print MetdatasDICT["CurrentMail"]
                CurrentMail = MetdatasDICT["CurrentMail"]
                print MetdatasDICT["FirstName"]
                FirstName = MetdatasDICT["FirstName"]
                print MetdatasDICT["LastName"]
                LastName = MetdatasDICT["LastName"]
                print MetdatasDICT["CurrentCompany"]
                CurrentCompany = MetdatasDICT["CurrentCompany"]
                print MetdatasDICT["STRUserUUID1"]
                STRUserUUID1 = MetdatasDICT["STRUserUUID1"]
                print MetdatasDICT["JobRole"]
                JobRole = MetdatasDICT["JobRole"]
            print "************DEBUG 4 ***********"
            f = request.files['file']
            f.save(secure_filename(f.filename))
            print "FILE SAVED LOCALY"
            return 'DATA (FILE AND METADATAS) posted'

api.add_resource(OPERATIONS, '/<string:inputs_id>')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port= 877)
