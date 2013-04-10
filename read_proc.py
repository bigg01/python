#!/usr/bin/env python
#! -*- coding: utf-8 -*

__author__ = "Oliver Guggenbuehl"
__copyright__ = "Copyright 2013, The GUOPY Project"
__credits__ = ["Oliver Guggenbuehl"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Oliver Guggenbuehl"
__email__ = "me@oliver-guggenbuehl.com"
__status__ = "Test"

import re

class readPROC(object):
  def __init__(self, data):
		self.FILE = ''
		self.FILE = data
		if self.FILE == 'CPU':
			self.FILE = '/proc/cpuinfo'

		elif self.FILE == 'MEM':
			self.FILE = '/proc/meminfo'
		else:
			print "using standard"
			self.FILE = '/proc/meminfo'

	def CPUF(self):
		pass

	def MEMF(self, f):
		for line in f.readlines():
			#line=line.strip('\n')
			line=line.strip('\n')
			#line=line.strip('\n')
			#line=line.split()
			Committed_AS = ""
			CommitLimit = "" 
			#print line.split()[:1]
			if re.search("Mem", line):
				print line
				#if len(line) > 1:
				#	print line[1]
			if re.search("CommitLimit", line):
				CommitLimit = line.split(':')[1].split(' ')[4]
				print CommitLimit
				

			if re.search("Committed_AS", line):
				Committed_AS =  line.split(':')[1].split(' ')[4]
				print Committed_AS


			if re.search("Swap", line):
				print line


		if Committed_AS is not None:
			if CommitLimit is not None:
				if Committed_AS > CommitLimit:
					print "To Much Memory Used"
				

		# for line in f:
		# 	print "juhu"
		# 	s = line.split(':')
		# 	print s[0],s[2]


	def readFS(self, data):
		print self.FILE
		f = open(self.FILE, 'r')
		#f = open('/proc/meminfo', 'r')
		self.MEMF(f)
		f.close

	def printOUT(self, ttt):



try:     
	ccc = readPROC('MEM')
	
	#cpu = ccc.readFS('CPU')
	#cpu = ccc.readFS('33')
	mem = ccc.readFS('MEM')
	#print mem
#print ('[ \033[1;42m' + mem +'\033[1;m ]') 

 	#return True 
except RuntimeError:
	print 'error '
	print RuntimeError 
	#print ('port:' + '\t' + port + "\t" + 'IP: '+ ip + '\t'+ '[ \033[1;41mCLOSED\033[1;m ]') 
	#return False
