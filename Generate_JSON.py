import json
import requests
import time
import random

start_time = time.time()
container_name_list = list()
ci_name_list = list()
attributes_output_list = list()
node_string_list = list()
edge_string_list = list()
container_count = 0
all_node_string = ''
all_edge_string = ''
json_string = ''
AE_url = 'http://54.68.184.172:8282/InCSE1/Team2AEx'

Parameter1 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '1'}
Parameter2 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '2'}
Parameter3 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '3'}
Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

r = requests.get(AE_url,params=Parameter2,headers = Header)
output_AE_2 = r.text
s = requests.get(AE_url,params=Parameter1,headers = Header)
output_AE_1 = s.text
attributes_output_list.append(output_AE_1)

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
								
def GetCIAttributes():
	container_name_list = GetChildList(output_AE_2, 'child-container List')
	for name in container_name_list:
		Container_URL = AE_url + '/%s' %(name)
		#print Container_URL
		r = requests.get(Container_URL, params = Parameter2, headers = Header)
		output_for_container = r.text
		ci_name_list = GetChildList(output_for_container, 'child-contentInstance List')
		for CI_Name in ci_name_list:
			CI_URL = Container_URL + '/%s' %(CI_Name)
			r = requests.get(CI_URL, params = Parameter1,headers = Header)
			output_for_CI = r.text
			print output_for_CI
			print'-------------------------------'

def GetContainerAttributes():
	container_name_list = GetChildList(output_AE_2, 'child-container List')
	for name in container_name_list:
		Container_URL = AE_url + '/%s' %(name)
		r = requests.get(Container_URL, params = Parameter1, headers = Header)
		output_for_container = r.text
		attributes_output_list.append(output_for_container)

def StripoffAttribute(input_json_string):
	input_json_string = json.loads(input_json_string)["output"]
	if (input_json_string["responseStatusCode"]==2002):
		resourceType = input_json_string["ResourceOutput"][0]["resourceType"]
		if resourceType == 'AE':
			print 'resourceType is...'
			print resourceType
			attributes=input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					global AE_id
					AE_id = item["attributeValue"]
					print 'AE_id is...'
					print AE_id
				if (item["attributeName"] == "resourceName"):
					global AE_name
					AE_name = item["attributeValue"]
					print 'AE_name is...'
					print AE_name
				if (item["attributeName"] == "parentID"):
					AE_parent = item["attributeValue"]
					print 'AE_parent is...'
					print AE_parent
				x = round(random.uniform(-100,100),3)
				y = round(random.uniform(-100,100),3)
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"resourceType\":\"%s\",\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":8.5},' %(AE_id, AE_name, resourceType,x ,y)
			node_string_list.append(node_string)
		if resourceType == 'container':
			print 'resourceType is...'
			print resourceType
			attributes=input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					container_id = item["attributeValue"]
					print 'container_id is...'
					print container_id #number
				if (item["attributeName"] == "resourceName"):
					container_name = item["attributeValue"]
					print 'container_name is...'
					print container_name #container0
				if (item["attributeName"] == "parentID"):
					a = len(item["attributeValue"].split('/'))
					container_parent = item["attributeValue"].split('/')[a-1]
					print 'container_parent is...'
					print container_parent #Team2AEx
					print AE_name
					if container_parent == AE_name:
						source_id = AE_id
						target_id = container_id
						print 'source_id is...'
						print source_id
						print 'target_id is...'
						print target_id
				x = round(random.uniform(-100,100),3)
				y = round(random.uniform(-100,100),3)
				edge_id = random.randint(0,100)
			edge_string = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(source_id, target_id, edge_id)
			edge_string_list.append(edge_string)		
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"resourceType\":\"%s\",\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":8.5},' %(container_id, container_name, resourceType,x ,y)
			node_string_list.append(node_string)
				

GetContainerAttributes()
print attributes_output_list
for string in attributes_output_list:
	StripoffAttribute(string)
for string in node_string_list:
	all_node_string += string
	if (string == node_string_list[-1]):
		all_node_string = all_node_string[:len(all_node_string)-1]
		#delete the last ","
node_start_string = '\"nodes\":['
node_end_string = ']}'
all_node_string = node_start_string + all_node_string + node_end_string
print 'this is the all_node_string'
print '----------------------------'
print all_node_string
print '----------------------------'
edge_start_string = '{\"edges\":['
edge_end_string = '],'
for string in edge_string_list:
	all_edge_string += string
	if string == edge_string_list[-1]:
		all_edge_string = all_edge_string[:len(all_edge_string)-1]
all_edge_string = edge_start_string + all_edge_string + edge_end_string
print 'this is the all_edge_string'
print '----------------------------'
print all_edge_string
print '----------------------------'
json_string = all_edge_string + all_node_string
text_file = open("generated.json", "w")
text_file.write(json_string)
text_file.close()
print 'Json has been successfully created'

end_time = time.time()
print end_time - start_time

