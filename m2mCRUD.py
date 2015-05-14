import requests
import json

#This file shows proof of concept CRUD using the new M2M standard

nodePath = 'InCSE1/myAE_Nik'
server = 'http://64.103.37.47:8888/'
URI = server + nodePath

#GET
headerGET = {'Content-Type': 'application/json', 'X-M2M-Origin': '//localhost:10000', 'X-M2M-RI': '12345'}
parameterGET = {'rcn': '4', 'drt': '1'}

#POST
#Change X-M2M-NM to the name you want to give the created resource
headerPOST = {'Content-Type': 'application/json', 'X-M2M-Origin': '//localhost:10000', 'X-M2M-RI': '12345', 'X-M2M-OT': 'NOW', 'X-M2M-NM': 'myAE_Nik1'}
parameterPOST_AE= {'ty': '2'}
parameterPOST_Resource{'ty': '3'}
contentPOST = {
	"aei":"myAE",
	"api":"myAE",
	"apn":"MyAE",
	"or":"http://hey/you"
}

#UPDATE
headerPUT = {'Content-Type': 'application/json', 'X-M2M-Origin': '//localhost:10000', 'X-M2M-RI': '12345', 'X-M2M-OT': 'NOW'}
contentPUT = {
	"aei":"AAA",
	"api":"BBB",
	"apn":"CCC",
	"or":"null"
}

#DELETE
headerDELETE = headerGET


def GET():
	print URI
	r = requests.get(URI, params = parameterGET, headers = headerGET)
	printStats(r)
	resourceOutputRaw = r.text
	resourceOutput = json.loads(resourceOutputRaw)['any']

def POST_AE():
	print URI
	r = requests.post(URI, params = parameterPOST_AE, headers = headerPOST, data = json.dumps(contentPOST))
	printStats(r)

def POST_Resource():
	print URI
	r = requests.post(URI, params = parameterPOST_Resource, headers = headerPOST)


#Currently getting Error 500
def PUT():
	print URI
	r = requests.put(URI, params = headerPUT, data = json.dumps(contentPUT))
	printStats(r)

#Currently getting Error 500
def DELETE():
	print URI
	r = requests.delete(URI, params = headerDELETE)
	printStats(r)

def printStats(r):
	print 'URL = ' + str(r.url)
	print 'Status Code = ' + str(r.status_code)
	print 'Server Returned = ' + str(r.text)





