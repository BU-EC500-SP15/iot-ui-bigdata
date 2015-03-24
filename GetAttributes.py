import json
import requests

Container_List = list()
CI_List = list()
def printStats():
    print r.url
    print r.status_code
    print r.text
AE_url = 'http://localhost:8282/InCSE1/Team2AEx'

Parameter1 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '1'}
Parameter2 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '2'}
Parameter3 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '3'}
Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

#print 'Get Request'
r = requests.get(AE_url,params=Parameter2,headers = Header)
output_for_AE = r.text
#print output_for_AE



# a function that can get a list of all the child(container name) in Team2AEx  
# I don't know if it works for other outputs or even for contentInstance
# I believe only minor changes will be made for getting a list of contentInstance
def GetChildList(output, attribute_name):
	temp_List = list()
	jOutput = json.loads(output)["output"]
	if (jOutput["responseStatusCode"]==2002):
		for index1,item in enumerate(jOutput["ResourceOutput"]):
			if (jOutput["ResourceOutput"][index1]["Attributes"]):
				Attributes=jOutput["ResourceOutput"][index1]["Attributes"]
				for index2,item in enumerate(Attributes):
					if (Attributes[index2]["attributeName"]==attribute_name):
						sStr = Attributes[index2]["attributeValue"]
						ChildStr=sStr[1:len(sStr)-1]
						for item in ChildStr.split(','):
							a = len(item.split('/'))
							if(a>0):
								temp_List.append(item.split('/')[a-1])
						return temp_List
								

#print'-------------------------------'
#print Container_List


	
def GetContainerAttributes():
	Container_List = GetChildList(output_for_AE, 'child-container List')
	for Container_Name in Container_List:
		Container_URL = AE_url + '/%s' %(Container_Name)
		#print Container_URL
		r = requests.get(Container_URL, params = Parameter1, headers = Header)
		output_for_container = r.text
		print output_for_container
		print'-------------------------------'
		#print output_for_container
		#print CI_List


def GetCIAttributes():
	Container_List = GetChildList(output_for_AE, 'child-container List')
	for Container_Name in Container_List:
		Container_URL = AE_url + '/%s' %(Container_Name)
		#print Container_URL
		r = requests.get(Container_URL, params = Parameter2, headers = Header)
		output_for_container = r.text
		CI_List = GetChildList(output_for_container, 'child-contentInstance List')
		for CI_Name in CI_List:
			CI_URL = Container_URL + '/%s' %(CI_Name)
			r = requests.get(CI_URL, params = Parameter1,headers = Header)
			output_for_CI = r.text
			print output_for_CI
			print'-------------------------------'
		#print output_for_container
		#print CI_List


#GetContainerAttributes()
GetCIAttributes()

