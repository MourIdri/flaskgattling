
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
import socket
import datetime
from multiprocessing import Pool
from multiprocessing import Process
from random import randint
from decimal import *

print "*** DEBUG FUNCTION This process has the pid", os.getpid()

client_name=socket.gethostname()
now = datetime.datetime.now()
Now_date=str(now.isoformat())

#Put your target server IP or URL and the average file size that will be uploaded
url = "http://demofrontapi.francecentral.cloudapp.azure.com"
url_send_write = url+":877/customerupdate"
url_send_read = url+":877/customerrequest"
FILESIZE=0.1


# Randomizing some inputs
def randomstring (size):
  randomstringvalue = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])
  return randomstringvalue

def DataCreation ():
  sizecharstring = 4
  CurrentMail_part1 = randomstring ( sizecharstring )
  sizecharstring = 3
  CurrentMail_part2 = randomstring ( sizecharstring )
  CurrentMail = CurrentMail_part1+"@"+CurrentMail_part2+".com"
  sizecharstring = 32
  STRUserUUID1 = randomstring ( sizecharstring )
  sizecharstring = 6
  FirstName = randomstring ( sizecharstring )
  sizecharstring = 6
  LastName = randomstring ( sizecharstring )
  sizecharstring = 4
  CurrentCompany = randomstring ( sizecharstring )
  sizecharstring = 4
  JobRole  = randomstring ( sizecharstring )
  #Filling data
  STRUserUUID1 = "EbDCxIfcGLRCLuxEv5WBVIiYT7EvjyYB"
  datas_write = {'CurrentMail': CurrentMail, 'STRUserUUID1': STRUserUUID1, 'FirstName': FirstName, 'LastName': LastName,  'CurrentCompany': CurrentCompany, 'JobRole': JobRole  }
  #datas_read = {'STRUserUUID1': STRUserUUID1 }
  STRUserUUID1_read = "EbDCxIfcGLRCLuxEv5WBVIiYT7EvjyYB"
  datas_read = {'STRUserUUID1': STRUserUUID1_read }
  return datas_write,datas_read



#Create a file filled with random caracteres
def create_random_file(FILESIZE):
  global filename
  #print "*** DEBUG CLIENT FUNCTION create_random_file // filesize is %sMB and owner is %s " % (str(FILESIZE),client_name)
  #filename="%sfilesize_%s_MB_%s.txt" % (client_name,str(FILESIZE),Now_date)
  filename="%s_datafile.txt" % (client_name)
  inc=Decimal(FILESIZE)
  with open(filename, 'w') as f:
    for i in range((inc*2**20)/512):
      f.write(os.urandom(512))
    f.close()
  return filename

#Create a function to send data using python requuest
def send_request_write(datas_var,url_var,thread_number):
  a = datetime.datetime.now()
  #print datas_var
  #print url_var
  payload = datas_var
  create_random_file(FILESIZE)
  local_file_to_send = filename
  files = {
         'json': (None, json.dumps(payload), 'application/json'),
         'file': (os.path.basename(local_file_to_send), open(local_file_to_send, 'rb'), 'application/octet-stream')
         }
  r = requests.post(url_var, files=files)
  b = datetime.datetime.now()
  c = b - a
  elapsed_time_request_microsecond = c.microseconds
  elapsed_time_request_millisec = (elapsed_time_request_microsecond/1000)
  print "*** DEBUG CLIENT FUNCTION WRITE THREAD %s / UPFILE AND DB TOOK %s MILS / STATUS CODE %s " % (thread_number,elapsed_time_request_millisec,r.status_code)

#creating a function to read data
def send_request_read(datas_var,url_var,thread_number):
  a = datetime.datetime.now()
  #print datas_var
  #print url_var
  payload = datas_var
  files = {
         'json': (None, json.dumps(payload), 'application/json')
         }
  r = requests.post(url_send_read, files=files)
  b = datetime.datetime.now()
  c = b - a
  elapsed_time_request_microsecond = c.microseconds
  elapsed_time_request_millisec = (elapsed_time_request_microsecond/1000)
  print "*** DEBUG CLIENT FUNCTION READ THREAD %s / DB SEARCH & READ TOOK %s MILS / STATUS CODE %s "  % (thread_number,elapsed_time_request_millisec,r.status_code)

#Create a random number of users to simulates random number of parrallele request
def parallel_requests_random (randmovalue,increment_counter):
  #print "*** DEBUG CLIENT FUNCTION // Total random request in parallele will be : %s " % (randmovalue)
  for i in range (0,randmovalue):
    datas_write,datas_read = DataCreation()
    thread_number = str(increment_counter)+str(i)
    Process_send_request_write = Process(target=send_request_write, args=(datas_write,url_send_write,thread_number, ))
    Process_send_request_read = Process(target=send_request_read, args=(datas_read,url_send_read,thread_number, ))
    Process_send_request_write.start()
    Process_send_request_read.start()
  print "\n "

#Call the random user call every X second to simulate the operation for a given periode of time.
def serial_calls_timer():
    i=0
    for i in range(0,3):
      #print "*** DEBUG CLIENT FUNCTION serial_calls_timer started hread # %s " % (i)
      increment_counter = i
      randmovalue = randint(1, 4)
      parallel_requests_random (randmovalue,increment_counter)
      time.sleep(1)#Wait X second and restart
      datas_write,datas_read = DataCreation()
      #thread_number = i 
      #send_request_read(datas_read,url_send_read,thread_number)
      #send_request_write(datas_write,url_send_write,thread_number)


serial_calls_timer()
