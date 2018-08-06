
#!/usr/bin/python
# sudo pip install inotify 


import os
from os import environ
import requests
import ast
import sys
import logging
import time
import datetime
import time
import json
import uuid
import sys
import logging
import subprocess
from subprocess import Popen, PIPE
from os.path import join, dirname

from flask import Flask, request , render_template
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_restful import Resource, Api


import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)




def loopApp():

	loop = 1
	while loop == 1:
		print "*** DEBUG SERVER FUNCTION restarter is starting"
		try:
			#popen = subprocess.Popen(wa_dir_watch, shell = True, stdin = None, stdout = subprocess.PIPE, stderr = subprocess.PIPE); (out, err) = popen.communicate()
			process = subprocess.call(['python', 'server_python_request_gattling_write.py', '&', 'python', 'server_python_request_gattling_read.py', '&'])
			#process = subprocess.Popen(wa_dir_watch, shell = True, stdout=subprocess.PIPE)
			#process = Popen(['wa_dir_watch', '/tmp/filename.swf', '-d'], stdout=PIPE, stderr=PIPE) stdout, stderr = process.communicate()
			#wa_dir_watch.ImageWrittenInFolder ()
			print ("\n*** DEBUG SERVER FUNCTION restarter retrying after Networking issue 1 ")
			continue 			

		except "*** DEBUG SERVER FUNCTION restarter retrying after issue 2":
			print ("\n*** DEBUG SERVER FUNCTION restarter retrying after issue 2 ")
			continue
		
		except '*** DEBUG SERVER FUNCTION restarter retrying after issue 3':
			print ("\n*** DEBUG SERVER FUNCTION restarter retrying after issue 3")
			continue
		

		except 'IOError':
			print ("\n*** DEBUG SERVER FUNCTION restarter retrying after Networking issue : IOError")
			continue
		 
		except KeyboardInterrupt:
			print ("\n*** DEBUG SERVER FUNCTION restarter retrying after Networking issue : stopped by user Ctr+C")
			quit() 
			



currentdirpath = os.getcwd()

TEMP1 = "TEMP_1"
TEMP2 = "TEMP_2" 
TEMP3 = "TEMP_3"
TEMP4 = "TEMP_4"

APPDIRS=[TEMP1,TEMP2,TEMP3,TEMP4]

for directory in APPDIRS:
	if not os.path.exists(directory):
		os.makedirs(directory)

 
loopApp()
