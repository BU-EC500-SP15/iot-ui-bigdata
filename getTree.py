#The getTree function will get the JSON attribute data of all containers
#and contentInstances that are below the root_node parameter passed.
#root_node is a string of the path to the node
#ie: root_node = 'InCSE1/Team2AEx'

#PSUEDO
#Get ATTR of container
  #If exists attribute container_list
    #for container in container_list                                    
      #GET ATTR of container and append to attributes_output_list
      #recurse GetWholeTree(container)
  #If exists attribute child_contentInstance_list
    #for contentInstance in child_contentInstance_list
    #GET ATTR of contextInstance and append to attributes_output_list
#Return

import json
import requests
import pdb

Parameter1 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '1'}
Parameter2 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '2'}
Parameter3 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '3'}
Parameter10 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '10'}
Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
attrOutputList = list()
root_node = 'InCSE1/Team2AEn'
server = 'http://54.68.184.172:8282/'

def getTree(attrOutputList,root_node):
    global errorFlag
    errorFlag = 0
    numChild = 0
    numContainer = 0
    numContentInstance = 0

    #Construct URI for root_node
    URI = server + str(root_node)
    print URI

    #Do GET request for attributes of container (p10)
    r = requests.get(URI, params = Parameter10, headers = Header)
    containerOutputRaw = r.text
    print containerOutputRaw
    containerOutput = json.loads(containerOutputRaw)['output']
    
    #Check that we got valid response
    if(checkValidResponse(containerOutput)== 0):
        return

    #Append Raw JSON Attributes to List
    attrOutputList.append(containerOutputRaw)

    #Check if container has children
    for attr in containerOutput['ResourceOutput'][0]['Attributes']:
        if(attr['attributeName'] == 'child-resource number'):
            numChild = attr['attributeValue']
            #Get number of children
            if(numChild  == "0"):
                #Found no children
                return
        if(attr['attributeName'] == 'Total Child Resource Number'):
            #Get number of children
            numChild = attr['attributeValue']
            if(numChild == "0"):
                #Found no children
                return
        if(attr['attributeName'] == 'Child-ResourceContainer Number'):
            #Get number of containers
            numContainer = attr['attributeValue']
        if(attr['attributeName'] == 'Child-ResourceContentInstance Number'):
            #Get number of contentInstances
            numContentInstance = attr['attributeValue']
    
    #Do 2nd GET request for list of children
    r = requests.get(URI, params = Parameter2, headers = Header)
    containerOutputCListRaw = r.text
    print containerOutputCListRaw
    containerOutputCList = json.loads(containerOutputCListRaw)['output']
    
    #Check that we got valid response
    if(checkValidResponse(containerOutputCList)== 0):
        return
    
    #Recurse getTree on every container in Child-Container List
    #Child-container List is string and therefore needs to be parsed
    for attr in containerOutputCList['ResourceOutput'][0]['Attributes']:
        if(attr['attributeName'] == 'child-container List'):
            print attr['attributeValue']
            #Parse Child-Container List
            containerList = attr['attributeValue'].split(', ')
            count = 0
            print 'numChild = ' + str(numChild) #TEST
            print 'numContainer = ' + str(numContainer) #TEST
            print 'numContentInstance = ' + str(numContentInstance) #TEST
            #Iterate and Recurse on every container
            for container in containerList:
                if(errorFlag == 1):
                    return
                count += 1
                #If 1 container -> remove [ and ]
                if(numContainer == '1'):
                    print container[1:-1]
                    getTree(attrOutputList,container[1:-1])
                    continue
                #First container -> remove [
                if(count == 1):
                    print container[1:] #TEST
                    getTree(attrOutputList,container[1:])
                    continue
                #Last container -> remove ]
                if(str(count) == numContainer):
                    print container[:-1] #TEST
                    getTree(attrOutputList,container[:-1])
                    continue
                #Other container -> remove nothing
                print container #TEST
                getTree(attrOutputList,container)
    #Get attributes of every content Instance in Child-contentInstance List
    #Child-contentInstance List is string and needs to be parsed
    for attr in containerOutputCList['ResourceOutput'][0]['Attributes']:
        if(attr['attributeName'] == 'child-contentInstance List'):
            print attr['attributeValue']
            #Parse child-contentInstance List
            contentInstanceList = attr['attributeValue'].split(', ')
            count = 0
            print 'numChild = ' + str(numChild) #TEST
            print 'numContainer = ' + str(numContainer) #TEST
            print 'numContentInstance = ' + str(numContentInstance) #TEST
            #Iterate through contentInstances
            for contentInstance in contentInstanceList:
                if(errorFlag == 1):
                    return
                count += 1
                #If 1 contentInstance -> remove [ and ]
                if(numContentInstance == '1'):
                    print contentInstance[1:-1] #TEST
                    #Construct URI for contentInstance
                    URI = server + str(contentInstance[1:-1])
                    
                    #GET request for Attributes of contentInstance
                    r = requests.get(URI, params = Parameter10, headers = Header)
                    contentInstanceOutputRaw = r.text
                    print contentInstanceOutputRaw #TEST
                    contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']
                    
                    #Check that we got valid response
                    if(checkValidResponse(containerOutput)== 0):
                        return
                    #Append Raw JSON Attributes to List
                    attrOutputList.append(containerOutputRaw) 
                    return
                #First contentInstance -> remove [
                if(count == 1):
                    print contentInstance[1:] #TEST
                    URI = server + str(contentInstance[1:])
                    
                    #GET request for Attributes of contentInstance
                    r = requests.get(URI, params = Parameter10, headers = Header)
                    contentInstanceOutputRaw = r.text
                    print contentInstanceOutputRaw  #TEST
                    contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']

                    #Check that we got valid response
                    if(checkValidResponse(containerOutput)== 0):
                        return
                    #Append Raw JSON Attributes to List
                    attrOutputList.append(containerOutputRaw)
                    continue
                
                #Last contentInstance -> remove ]
                if(str(count) == numContentInstance):
                    print contentInstance[:-1]
                    URI = server + str(contentInstance[:-1])
                    
                    #GET request for Attributes of contentInstance
                    r = requests.get(URI, params = Parameter10, headers = Header)
                    contentInstanceOutputRaw = r.text
                    print contentInstanceOutputRaw  #TEST
                    contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']
                    
                    #Check that we got valid response
                    if(checkValidResponse(containerOutput)== 0):
                        return
                    #Append Raw JSON Attributes to List
                    attrOutputList.append(containerOutputRaw)
                    return
                
                #Other contentInstance -> remove nothing
                print contentInstance
                URI = server + str(contentInstance[1:])
                
                #GET request for Attributes of contentInstance                                                          
                r = requests.get(URI, params = Parameter10, headers = Header)
                contentInstanceOutputRaw = r.text
                print contentInstanceOutputRaw  #TEST                                                                  
                contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']
                
                #Check that we got valid response                                                                       
                if(checkValidResponse(containerOutput)== 0):
                    return
                #Append Raw JSON Attributes to List                                                                     
                attrOutputList.append(containerOutputRaw)
    print attrOutputList
    return


def checkValidResponse(containerOutput):
    if(containerOutput["responseStatusCode"]==2002):
        return 1
    else:
        print 'ERROR - invalid response from server'
        errorFlag = 1
        return 0

getTree(attrOutputList,root_node)





