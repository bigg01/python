#import library to do http requests:
import urllib2
 

import pprint
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
def getxml(enc): 
  #download the file:
  file = urllib2.urlopen(enc)
  #convert to string:
  data = file.read()
  #close file because we dont need it anymore:
  file.close()
  #parse the xml you downloaded
  dom = parseString(data)

  #print dom
  #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
  #xmlTag = dom.getElementsByTagName('MGMTDNSNAME')[0].toxml()
  #xmlTag = dom.getElementsByTagName('MGMTDNSNAME')[0].toxml()
  #print dom.getElementsByTagName('MGMTDNSNAME')
  print enc

      # <SPN> BSN
  for node in dom.getElementsByTagName('MGMTDNSNAME'):
    xmlTag=node.toxml()
    #strip off the tag (<tag>data</tag>  --->   data):
    xmlData=xmlTag.replace('<MGMTDNSNAME>','').replace('</MGMTDNSNAME>','')
    #print out the xml tag and data in this format: <tag>data</tag>
    #print xmlTag
    #just print the data
    systems[enc] = { 'Server' : xmlData}
    print xmlData
  
  for node in dom.getElementsByTagName('RACK'):
    xmlTag=node.toxml()
    #strip off the tag (<tag>data</tag>  --->   data):
    xmlData=xmlTag.replace('<RACK>','').replace('</RACK>','')
    #print out the xml tag and data in this format: <tag>data</tag>
    #print xmlTag
    #just print the data
    print xmlData


  for node in dom.getElementsByTagName('BSN'):
    xmlTag=node.toxml()
    #strip off the tag (<tag>data</tag>  --->   data):
    xmlData=xmlTag.replace('<BSN>','').replace('</BSN>','')
    #print out the xml tag and data in this format: <tag>data</tag>
    #print xmlTag
    #just print the data
    print xmlData  


  for node in dom.getElementsByTagName('SPN'):
    xmlTag=node.toxml()
    #strip off the tag (<tag>data</tag>  --->   data):
    xmlData=xmlTag.replace('<SPN>','').replace('</SPN>','')
    #print out the xml tag and data in this format: <tag>data</tag>
    #print xmlTag
    #just print the data
    print xmlData

systems = {}

getxml('http://mpzhbencd03oa1/xmldata?item=all')
getxml('http://mpzhbencd04oa1/xmldata?item=all')
print systems
