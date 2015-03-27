#This tree builder will let you choose how many container you want to add in an AE 
#and how many contentInstance you want to add in each container 
#You should have already created the AE in the tree and change the AE_url of your AE name
import json
import requests

def print_container_Stats():
    print container_output.url
    print container_output.status_code
    print container_output.text

def print_contentInstance_Stats():
    print contentInstance_output.url
    print contentInstance_output.status_code
    print contentInstance_output.text

AE_url = 'http://54.68.184.172:8282/InCSE1/Team2AEx'

Parameter = {'from': 'http:localhost:10000', 'requestIdentifier': '12345'}
Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

container_number = 10
#This is the number how many container you want to add in AE
contentInstance_number = 2
#This is the number how many contentInstance you want to add in each container
for container_count in xrange(0,container_number):
    #This for loop will create container in AE
    temp1 = str(container_count)
    container_name = 'container' + temp1
    #Create container
    Data_container =  "{\"from\":\"http:localhost:10000\",\"requestIdentifier\":\"12345\",\"resourceType\":\"container\",\"content\":{\"labels\":\"Test_For_Python_Code\",\"resourceName\":\"%s\"}}" %(container_name)
    print 'Post Request Creating container'
    container_output = requests.post(AE_url, params= Parameter, headers = Header, data= Data_container)
    print_container_Stats()
    for contentInstance_count in xrange(0,contentInstance_number):
    #This for loop will create contentInstance in each container
        temp2 = str(contentInstance_count)
        contentInstance_name = 'contentInstance' + temp2
        #Create contentInstance
        container_url = AE_url + '/%s' %(container_name)
        Data_contentInstance = "{\"from\":\"http:localhost:10000\",\"requestIdentifier\":\"12345\",\"resourceType\":\"contentInstance\",\"content\":{\"labels\":\"Test_For_Python_Code\",\"resourceName\":\"%s\"}}" %(contentInstance_name)
        print 'Post Request Creating contentInstance'
        contentInstance_output = requests.post(container_url, params= Parameter, headers = Header, data= Data_contentInstance)
        print_contentInstance_Stats()
