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
 
                                    #print line.split()[:1]
                                    if re.search("Mem", line):
                                                print line
                                                #if len(line) > 1:
                                                #          print line[1]
                                    if re.search("Commi", line):
                                                print line
                                                print line.strip('\t')[:]
                                    if re.search("Swap", line):
                                                print line
 
            def readFS(self, data):
 
                        f = open(self.FILE, 'r')
                        #f = open('/proc/meminfo', 'r')
                        self.MEMF(f)
                        f.close
 
# def readPROC():
#          f = open('/proc/meminfo', 'r')
#          for line in f.readlines():
#                      line=line.strip('\n')
#                      #print line.split()[:1]
#                      if re.search("Mem", line):
#                                  print line
#                      if re.search("Commi", line):
#                                  print line
#                      if re.search("Swap", line):
#                                  print line
#          f.close
 
 
#if __name__ == '__main__':
            #readPROC()
 
 
 
try:    
            ccc = readPROC('MEM')
           
            cpu = ccc.readFS('CPU')
            cpu = ccc.readFS('33')
            #mem = ccc.readFS('MEM')
            #print mem
#print ('[ \033[1;42m' + mem +'\033[1;m ]')
 
           #return True
except RuntimeError:
            print 'error '
            print RuntimeError
            #print ('port:' + '\t' + port + "\t" + 'IP: '+ ip + '\t'+ '[ \033[1;41mCLOSED\033[1;m ]')
            #return False
