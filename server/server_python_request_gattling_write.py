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
            return 'Hello World! Welcome to the Azure MySQL and Blob API Wrapper Can try using Curl  '

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
            #now store data in a MysqlDatabase
            str_json_echoed = json.dumps(MetdatasDICT)
            script_tosend_to = "db_operations_v9_write.py"
            python_cmd = "python %s" %(script_tosend_to)
            cmd= "echo '" + str_json_echoed + "' | "+ python_cmd
            os.system(cmd)
            return '*** DEBUG SERVER FUNCTION customerupdate FNISHED '

        @app.route('/customerrequest',methods=['POST'])
        def customerrequest():
            RequestValues = request.values
            RequestForm = request.form
            so = RequestForm
            json_of_metadatas = so.to_dict(flat=False)
            MetdatasFromJSON = json_of_metadatas['json']
            MetdatasFromJSON0 = MetdatasFromJSON[0]
            strMetdatasFromJSON0 = str(MetdatasFromJSON0)
            MetdatasDICT = ast.literal_eval(strMetdatasFromJSON0)
            print MetdatasDICT
            for key in MetdatasDICT :
                STRUserUUID1 = MetdatasDICT["STRUserUUID1"]
            keyword = STRUserUUID1
            #getting the file and storing it
            #now store data in a MysqlDatabase
            str_json_echoed = json.dumps(MetdatasDICT)
            script_tosend_to = "db_operations_v9_read.py"
            python_cmd = "python %s" %(script_tosend_to)
            cmd= "echo '" + str_json_echoed + "' | "+ python_cmd
            os.system(cmd)
            return '*** DEBUG SERVER FUNCTION customerrequest FNISHED '


print "*** DEBUG FUNCTION This process has the pid", os.getpid()

api.add_resource(OPERATIONS, '/<string:inputs_id>')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port= 877)