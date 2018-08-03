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


import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)

app = Flask(__name__)
api = Api(app)
app.debug = True

class OPERATIONS(Resource):
        @app.route('/',methods=['GET'])
        def hello_world():
            return 'Hello World! Welcome to the Azure MySQL and Blob API Wrapper READER '

        @app.route('/customerupdate',methods=['POST'])
        def customerupdate():
            RequestValues = request.values
            RequestForm = request.form
            so = RequestForm
            json_of_metadatas = so.to_dict(flat=False)
            MetdatasFromJSON = json_of_metadatas['json']
            MetdatasFromJSON0 = MetdatasFromJSON[0]
            strMetdatasFromJSON0 = str(MetdatasFromJSON0)
            MetdatasDICT = ast.literal_eval(strMetdatasFromJSON0)
            #getting the file and storing it
            f = request.files['file']
            f.save(secure_filename(f.filename))
            print "*** DEBUG FUNCTION FILE SAVED LOCALY"
            #now store data in a MysqlDatabase
            str_json_echoed = json.dumps(MetdatasDICT)
            print "*** DEBUG FUNCTION customerupdate json_echoed...%s" % (str_json_echoed )
            script_tosend_to = "db_operations_v9_write.py"
            python_cmd = "python %s" %(script_tosend_to)
            cmd= "echo '" + str_json_echoed + "' | "+ python_cmd
            print "*** DEGUB FUNCTION Will apply CMD :  \n  "
            print "\n*** DEBUG FUNCTION customerupdate cmd...%s\n" % (cmd )
            os.system(cmd)
            print "\n*** DEGUB FUNCTION.py applied CMD "
            return '*** DEBUG FUNCTION customerupdate FNISHED '

        @app.route('/customerrequest',methods=['POST'])
        def customerrequest():
            print "*** DEBUG FUNCTION customerrequest 0"
            RequestValues = request.values
            print "*** DEBUG FUNCTION customerrequest 1"
            RequestForm = request.form
            print "*** DEBUG FUNCTION customerrequest 2"
            so = RequestForm
            print "*** DEBUG FUNCTION customerrequest 3"
            json_of_metadatas = so.to_dict(flat=False)
            MetdatasFromJSON = json_of_metadatas['json']
            MetdatasFromJSON0 = MetdatasFromJSON[0]
            strMetdatasFromJSON0 = str(MetdatasFromJSON0)
            print "*** DEBUG FUNCTION customerrequest 4"

            MetdatasDICT = ast.literal_eval(strMetdatasFromJSON0)
            print MetdatasDICT
            for key in MetdatasDICT :
                STRUserUUID1 = MetdatasDICT["STRUserUUID1"]
            keyword = STRUserUUID1
            #getting the file and storing it
            print "*** DEBUG FUNCTION FILE SAVED LOCALY"
            #now store data in a MysqlDatabase
            #str_json_echoed = str(json_echoed)
            str_json_echoed = json.dumps(MetdatasDICT)
            print "*** DEBUG FUNCTION customerupdate json_echoed...%s" % (str_json_echoed )
            script_tosend_to = "db_operations_v9_read.py"
            python_cmd = "python %s" %(script_tosend_to)
            cmd= "echo '" + str_json_echoed + "' | "+ python_cmd
            print "*** DEGUB FUNCTION Will apply CMD :  \n  "
            print "\n*** DEBUG FUNCTION customerupdate cmd...%s\n" % (cmd )
            os.system(cmd)
            print "\n*** DEGUB FUNCTION.py applied CMD "
            return '*** DEBUG FUNCTION customerrequest FNISHED '


print "*** DEBUG FUNCTION This process has the pid", os.getpid()

api.add_resource(OPERATIONS, '/<string:inputs_id>')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port= 887)