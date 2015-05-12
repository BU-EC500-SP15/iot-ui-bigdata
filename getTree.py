#!/usr/bin/env python

    #PSUEDO
    #getTree(attrOutputList,resource,depth):
        #GET Attr of passed Resource
        #Append Attr to attrOutputList
        #For every resource (container/AE) in resourceOutput
            #getNumChildren(resource)
            #if numChildren == 0
                #continue - nothing to do
            #else
                #Do 2nd Get request for child_list
                #if(checkValidResponse):
                    #for every child in child_list
                        #if child is contentInstance
                            #GET child Attributes
                            #append Attributes to attrOutputList
                            #continue
                        #if child is container
                            #recurse getTree(attrOutputList,child,depth)

import json
import requests
import cgi
import cgitb

#resultContent = 1 -> Attributes Only
Parameter1 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '1'}

#resultContent = 5 -> Attributes & Child_List (No # Children)
Parameter5 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '5'}

#resultContent = 6 -> Child List Only
Parameter6 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '6'}

#resultContent = 10 -> Attributes & # Children
Parameter10 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '10'}

Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
attrOutputList = list()
root_node = 'InCSE1'
server = 'http://54.68.184.172:8282/'
depthToNumObj = dict()
depthToCount = dict()
depthToY = dict()
nodeStringList = list()
edgeStringList = list()
container_id_list = list()
container_name_list = list()
allNodeString = ''
allEdgeString = ''
pathwithid = dict()


#Set InitialDepth
depth = 0
#Exception if root_node is not CSEBase
rootDepth = root_node.count('/')
if(rootDepth >= 1):
    depth = -1

depthToNumObj[0] = 1

def getTree(attrOutputList,root_node,depth):
    #If we encounter an error - breaks us out of our recursion
    global errorFlag
    errorFlag = 0

    #Info we need
    numChildren = {'numChild' : '0', 'numContainer' : '0', 'numContentInstance' : '0'}

    #Current depth in tree
    depth += 1

    #Construct URI for root_node
    URI = server + str(root_node)
    print URI

    #Do GET request for attributes of object (p10)
    r = requests.get(URI, params = Parameter10, headers = Header)
    resourceOutputRaw = r.text
    #print resourceOutputRaw
    resourceOutput = json.loads(resourceOutputRaw)['output']
    
    #Check that we got valid response
    if(checkValidResponse(resourceOutput)== 0):
        return

    #Append Raw JSON Attributes to List
    attrOutputList.append(resourceOutputRaw)

    temp = 0
    #Update Num Containers/contentInstances in Depth Hashtable
    #This tells us how many objects are in each depth level
    if(depthToNumObj.has_key(depth)):
        #If key already exists, grab current value
        temp = depthToNumObj.get(depth)

    if(depth != 0):
        depthToNumObj[depth] = (temp + len(resourceOutput['ResourceOutput']))

    #Iterate through every resource (usually one, except for AE which has multiple)
    for x in range(0, len(resourceOutput['ResourceOutput'])):
        #Check if container/AE has children
        success = checkNumChildren(resourceOutput,x, numChildren)
        printDebugInfo(numChildren,depth) #DEBUG
        if(numChildren['numChild'] == '0' or (success == 0)):
            continue

        #Do 2nd GET request for list of children
        #This get will be redone x # of times (only need once)
        r = requests.get(URI, params = Parameter6, headers = Header)
        resourceOutputCListRaw = r.text
        resourceOutputCList = json.loads(resourceOutputCListRaw)['output']
        print resourceOutputCList
        print resourceOutputCListRaw
        
        #Check that we got valid response
        if(checkValidResponse(resourceOutputCList)== 0):
            return
        
        #Recurse getTree on every container in Child-Container List
        #Child-container List is string and therefore needs to be parsed
        for attr in resourceOutputCList['ResourceOutput'][x]['Attributes']:
            if(attr['attributeName'] == 'child-container List'):
                print attr['attributeValue']
                #Parse Child-Container List
                containerListRaw = attr['attributeValue'][1:-1]
                print containerListRaw
                containerList = containerListRaw.split(', ')
                printDebugInfo(numChildren,depth) #DEBUG
                for container in containerList:
                    if(errorFlag == 1):
                        return
                    print container
                    getTree(attrOutputList,container,depth)

        #Get attributes of every content Instance in Child-contentInstance List
        #Child-contentInstance List is string and needs to be parsed
        for attr in resourceOutputCList['ResourceOutput'][x]['Attributes']:
            if(attr['attributeName'] == 'child-contentInstance List'):
                print attr['attributeValue']
                #Parse child-contentInstance List
                contentInstanceListRaw = attr['attributeValue'][1:-1]
                print contentInstanceListRaw
                contentInstanceList = contentInstanceListRaw.split(', ')
                printDebugInfo(numChildren,depth) #DEBUG
                print contentInstanceList
                for contentInstance in contentInstanceList:
                    if(errorFlag == 1):
                        return
                    print contentInstance
                    getContentInstance(attrOutputList,contentInstance,depth+1)
    
    #Print Final JSON Output
    #if(depth == 1):
        #print attrOutputList
    if(errorFlag == 1):
        print 'ERROR: invalid response from server check log'
    return

def checkNumChildren(resourceOutput,x,numChildren):
    try:
        for attr in resourceOutput['ResourceOutput'][x]['Attributes']:
            if(attr['attributeName'] == 'child-resource number'):
                numChildren['numChild'] = attr['attributeValue']
                #Get number of children
                if(numChildren['numChild']  == "0"):
                    #Found no children
                    return
            if(attr['attributeName'] == 'Total Child Resource Number'):
                #Get number of children
                numChildren['numChild'] = attr['attributeValue']
                if(numChildren['numChild'] == "0"):
                    #Found no children
                    return
            if(attr['attributeName'] == 'Child-ResourceContainer Number'):
                #Get number of containers
                numChildren['numContainer'] = attr['attributeValue']
            if(attr['attributeName'] == 'Child-ResourceContentInstance Number'):
                #Get number of contentInstances
                numChildren['numContentInstance'] = attr['attributeValue']
    except KeyError:
        print 'Error: No Attributes field in Resource'
        return 0
    return 1

def getContentInstance(attrOutputList,contentInstancePath, depth):
    try:    
        ##print contentInstancePath
        URI = server + str(contentInstancePath)

        #GET request for Attributes of contentInstance
        r = requests.get(URI, params = Parameter10, headers = Header)
        contentInstanceOutputRaw = r.text
        #print contentInstanceOutputRaw  #TEST
        contentInstanceOutput = json.loads(contentInstanceOutputRaw)['output']
        
        #Check that we got valid response                                                  
        if(checkValidResponse(contentInstanceOutput)== 0):
            return
        
        #Append Raw JSON Attributes to List
        attrOutputList.append(contentInstanceOutputRaw)
        
        #Update num containers/contentInstances in depth hashtable
        temp = 0
        if(depthToNumObj.has_key(depth)):
            #Get existing value of key depth
            temp = depthToNumObj.get(depth)
            
        depthToNumObj[depth] = (temp + 1)
        return
    except ValueError:
        print "Content-Type: text/html\n"
        print 'Error getting contentInstance'
        exit()

def checkValidResponse(containerOutput):
    return 1
    if(containerOutput["responseStatusCode"]==2002):
        return 1
    else:
        print 'ERROR - invalid response from server'
        errorFlag = 1
        return 0

def printDebugInfo(numChildren,depth):
    print 'numChild = ' + str(numChildren['numChild']) #TEST
    print 'numContainer = ' + str(numChildren['numContainer']) #TEST
    print 'numContentInstance = ' + str(numChildren['numContentInstance']) #TEST
    print 'Depth = ' + str(depth)

def generateJsonString(rawInput):
    attrDict = dict()
    sourceId = 0
    targetId = 0
    resourceType = json.loads(rawInput)["output"]["ResourceOutput"][0]["resourceType"]
    rawInput = json.loads(rawInput)["output"]["ResourceOutput"][0]["Attributes"]
    for item in rawInput:
        attrDict[item["attributeName"]] = item["attributeValue"]
    #generate JSON edge string start
    fullPath = attrDict["parentID"] + '/' + attrDict["resourceName"]
    depth = fullPath.count('/') - rootDepth
    depthToCount[depth] += 1
    pathwithid[fullPath] = attrDict["resourceID"]
    for parent in pathwithid.keys():
        if (attrDict["parentID"] == parent):
            sourceId = pathwithid[parent]
            targetId = attrDict["resourceID"]
            global edgeId
            edgeId += 1
            edgeString = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(sourceId, targetId, edgeId)
            edgeStringList.append(edgeString)
    #generate JSON edge string end
    #generate JSON node string start
    stringOne = '{'
    idString = '\"id\":' + '\"' + attrDict["resourceID"] + '\"' + ','
    nodeString = stringOne + idString
    #del attrDict["resourceID"]
    labelString = '\"label\":' +  '\"' + attrDict["resourceName"] + '\"'  + ','
    nodeString += labelString
    #del attrDict["resourceName"]
    nodeString += '\"attributes\":{'
    for attrName in attrDict.keys():
        if (attrName == 'resourceID' or attrName == 'resourceName'):
            continue
        nodeString += '\"' + attrName + '\"' + ':' + '\"' + attrDict[attrName] + '\"' + ','
    nodeString = nodeString[:len(nodeString) - 1]
    #eliminate last ',' in attribute node string
    x = depth * 1000
    y = depthToY[depth] - (depthToCount[depth] - 1) * 500
    size = 0
    color = ''
    if resourceType == 'AE':
        size = 15
        color = 'rgb(255,204,102)'
    elif resourceType == 'container':
        size = 10
        color = '#36e236'
    elif resourceType == 'contentInstance(latest-allAttributes)':
        size = 5
        color = '#3636e2'
    nodeString += '},\"x\":%s,\"y\":%s,\"color\":\"%s\",\"size\":%s},' %(x, y, color, size)
    #generate JSON node string end
    ##print nodeString
    ##print attrDict
    nodeStringList.append(nodeString)

getTree(attrOutputList,root_node,depth)

print '\nDepth to Num Containers/contentInstances Pairs'
print depthToNumObj.items()
for depth in depthToNumObj.keys():
    depthToCount[depth] = 0

for depth, num in depthToNumObj.iteritems():
    #if num is odd
    if (num % 2 == 1):
        depthToY[depth] = (num - 1) / 2 * 500
    #if num is even
    if (num % 2 == 0):
        depthToY[depth] = num / 2 * 500 - 250

if(rootDepth == 0):
    tempCSE1 = attrOutputList[0]
    attrOutputList.pop(0)
    firstString = '{\"output\":{\"responseStatusCode\":2002,\"ResourceOutput\":['
    lastString = ']}}'
    for x in xrange(depthToNumObj[1]):
        rawString = firstString + json.dumps(json.loads(tempCSE1)["output"]["ResourceOutput"][x]) + lastString
        attrOutputList.insert(x, rawString)
    #initial for InCSE1 node
    pathwithid['InCSE1'] = 10000
    cse1String = '{\"id\":10000,\"label\":\"InCSE1\",\"attributes\":{\"labels\":\"This is InCSE1\",\"resourceType\":\"cseBase\"},\"x\":0,\"y\":0,\"color\":\"rgb(240,0,0)\",\"size\":20},'
    nodeStringList.append(cse1String)

#initial for JSON string attributes
edgeId = 0
for raw in attrOutputList:
    generateJsonString(raw)
##print nodeStringList
##print edgeStringList
for string in nodeStringList:
    allNodeString += string
    if (string == nodeStringList[-1]):
        allNodeString = allNodeString[:len(allNodeString)-1]
nodeStartString = '\"nodes\":['
nodeEndString = ']}'
allNodeString = nodeStartString + allNodeString + nodeEndString
#print 'this is the allNodeString'
#print '----------------------------'
#print allNodeString
#print '----------------------------'
edge_start_string = '{\"edges\":['
edge_end_string = '],'
for string in edgeStringList:
   allEdgeString += string
   if string == edgeStringList[-1]:
       allEdgeString = allEdgeString[:len(allEdgeString)-1]
allEdgeString = edge_start_string + allEdgeString + edge_end_string
#print 'this is the allEdgeString'
#print '----------------------------'
#print allEdgeString
#print '----------------------------'
json_string = allEdgeString + allNodeString
#print json_string
parsed = json.loads(json_string)
pretty_json_string = json.dumps(parsed, indent=4, sort_keys=True)
text_file = open("network/data/iot.json", "w")
text_file.write(pretty_json_string)
text_file.close()
print "Content-Type: text/html\n"
print 'iot.json has been successfully created'
