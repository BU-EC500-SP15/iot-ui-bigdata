import json
import requests

root_url = 'http://54.68.184.172:8282/InCSE1'
delete_url = 'http://54.68.184.172:8282/InCSE1'

headers = {'from' : 'http:localhost:10000', 'requestIdentifier' : '12345', 'resultContent' : '1', 'Content-Type' : 'application/json', 'Accept' : 'application/json'}

Data = {
    "from": "http:localhost: 10000",
    "requestIdentifier": "12345",
    "resourceType": "container",
    "content":
        {
        "labels": "cookies" ,
        "resourceName": "cn6"
        }
}

def printStats():
    print r.url
    print r.status_code
    print r.text

#Simple GET Request
print 'Get Request'
r = requests.get(root_url,params= headers)
printStats()

#Simple DELETE Request
print 'Delete Request'
#r = requests.delete(delete_url,params=headers)
#printStats()

#Simple POST Request
print 'Post Request'
#r = requests.post(root_url, params= headers, data= json.dumps(Data))
#printStats()

#Simple PUT Request
print 'Put Request'
#r = requests.put(root_url, params= headers, data= json.dumps(Data))
#printStats()
