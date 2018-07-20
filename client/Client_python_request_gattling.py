
import os
import threading
import multiprocessing  
import time
import logging
import json
import time
import datetime
import shlex
import subprocess
import pprint 
import sys
import uuid
import requests
import string
import random

sizecharstring = 4 
def randomstring (size):
  randomstringvalue = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(sizecharstring)])
  return randomstringvalue

datas = {'CurrentMail': "CurrentMail", 'STRUserUUID1': "STRUserUUID1", 'FirstName': "FirstName", 'LastName': "LastName",  'CurrentCompany': "CurrentCompany", 'JobRole': "JobRole"  }
#url = "http://frontwebappmain:80/customerupdate"
url = "http://127.0.0.1:877/customerupdate"

def send_request(datas,url):
  a = datetime.datetime.now()
  #payload = {"param_1": "value_1", "param_2": "value_2"}
  payload = datas
  local_file_to_send = 'filesize_1MB.txt' 
  files = {
         'json': (None, json.dumps(payload), 'application/json'),
         'file': (os.path.basename(local_file_to_send), open(local_file_to_send, 'rb'), 'application/octet-stream')
         }
  r = requests.post(url, files=files)
  b = datetime.datetime.now()
  c = b - a
  elapsed_time_request_microsecond = c.microseconds
  elapsed_time_request_millisec = (elapsed_time_request_microsecond/1000)
  print "*** REQUEST TOOK %s IF FORMAT MS" % elapsed_time_request_millisec


def runInParallel(*fns):
  proc = []
  for fn, arg in fns:
    p = threading.Thread(target=fn, args=arg)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

#RUN ONLY ONE THREAD
#runInParallel((send_request,(datas,url,)),)
#RUN 5 THREADS IN //
runInParallel((send_request,(datas,url,)),(send_request,(datas,url,)),(send_request,(datas,url,)),(send_request,(datas,url,)),(send_request,(datas,url,)))



