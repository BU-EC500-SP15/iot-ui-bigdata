#This function will be called via AJAX by the front-end
#It will return the JSON for the most recent contentInstance

import requests
import json
import sys

def getLatest(containerURI):
    #containerURI is path to container
    server = 'http://54.68.184.172:8282/'
    latestURI = server + containerURI + '/latest'

    Parameter = {'from': 'http:localhost:10000', 'requestIdentifier': '12345'}
    Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    #Instantiate error Flag
    global errorFlag
    errorFlag = 0

    #Do GET request for latest contextInstance in container
    r = requests.get(latestURI, params = Parameter, headers = Header)
    contentInstanceOutputRaw = r.text
    print contentInstanceOutputRaw
    contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']

    #Check JSON return is valid
    if(contentInstanceOutput["responseStatusCode"] != 2002):
        errorFlag = 1
        print 'ERROR: Request for Latest contentInstance was unsuccesful'
    
    #QINGQING - I can print the JSON to a .json file on the server
    #Or I can just return the JSON through your AJAX call
    #Let me know which you prefer

#containerURI = 'InCSE1/Team2AEn/C1' #TEST VALUE

#This is the argument passed by the AJAX call
#Test this in cmd prompt by doing:
#python getLatest.py 'InCSE1/Team2AEn/C1'
containerURI = sys.argv[1]
print containerURI
getLatest(containerURI)
