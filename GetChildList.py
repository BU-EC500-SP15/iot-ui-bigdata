import json
import requests

output = '{"output":{"responseStatusCode":2002,"ResourceOutput":[{"resourceType":"AE","resourceID":"1415208429","Attributes":[{"attributeName":"child-container List","attributeValue":"[InCSE1/Team2AEx/container4, InCSE1/Team2AEx/container3, InCSE1/Team2AEx/container2, InCSE1/Team2AEx/container1, InCSE1/Team2AEx/container0, InCSE1/Team2AEx/container5, InCSE1/Team2AEx/container6, InCSE1/Team2AEx/container7, InCSE1/Team2AEx/container8, InCSE1/Team2AEx/container9]"}]}]}}'


# a function that can get a list of all the child(container name) in Team2AEx  
# I don't know if it works for other outputs or even for contentInstance
# I believe only minor changes will be made for getting a list of contentInstance
def GetChildList():
	if (jOutput["responseStatusCode"]==2002):
		for index1,item in enumerate(jOutput["ResourceOutput"]):
			if (jOutput["ResourceOutput"][index1]["Attributes"]):
				Attributes=jOutput["ResourceOutput"][index1]["Attributes"]
				for index2,item in enumerate(Attributes):
					if (Attributes[index2]["attributeName"]=="child-container List"):
						sStr = Attributes[index2]["attributeValue"]
						ChildStr=sStr[:len(sStr)-1]
						for item in ChildStr.split(','):
								a = len(item.split('/'))
								if(a>0):
									print item.split('/')[a-1]

GetChildList()
