import json
import requests
import time
import random
import pdb

Parameter1 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '1'}
Parameter2 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent' : '2'}
Parameter3 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '3'}
Parameter10 = {'from': 'http:localhost:10000', 'requestIdentifier': '12345', 'resultContent': '10'}
Header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

start_time = time.time()
container_name_list = list()
ci_name_list = list()
attributes_output_list = list()
node_string_list = list()
edge_string_list = list()
container_id_list = list()
container_name_list = list()
container_count = 0
all_node_string = ''
all_edge_string = ''
json_string = ''
AE_url = 'http://54.68.184.172:8282/InCSE1/Team2AEx'
edge_id = 0
x_AE = 0
y_AE = 0
x_container= -1000
y_container = 200
x_CI = -2000
y_CI = 600

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
		r = requests.get(Container_URL, params = Parameter2, headers = Header)
		output_for_container = r.text
		ci_name_list = GetChildList(output_for_container, 'child-contentInstance List')
		for CI_Name in ci_name_list:
			CI_URL = Container_URL + '/%s' %(CI_Name)
			r = requests.get(CI_URL, params = Parameter1,headers = Header)
			output_for_CI = r.text
			attributes_output_list.append(output_for_CI)

def GetContainerAttributes():
	container_name_list = GetChildList(output_AE_2, 'child-container List')
	for name in container_name_list:
		Container_URL = AE_url + '/%s' %(name)
		r = requests.get(Container_URL, params = Parameter1, headers = Header)
		output_for_container = r.text
		attributes_output_list.append(output_for_container)

def Generate_json_string(input_json_string):
	global x_AE, y_AE, x_container, y_container, x_CI, y_CI
	input_json_string = json.loads(input_json_string)["output"]
	if (input_json_string["responseStatusCode"]==2002):
		resourceType = input_json_string["ResourceOutput"][0]["resourceType"]
		if resourceType == 'AE':
			attributes=input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					global AE_id
					AE_id = item["attributeValue"]
				if (item["attributeName"] == "resourceName"):
					global AE_name
					AE_name = item["attributeValue"]
				if (item["attributeName"] == "parentID"):
					AE_parent = item["attributeValue"]
			
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"resourceType\":\"%s\",\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":8.5},' %(AE_id, AE_name, resourceType, x_AE, y_AE)
			node_string_list.append(node_string)
		if resourceType == 'container':
			attributes = input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					global container_id
					container_id = item["attributeValue"]
					container_id_list.append(container_id)
				if (item["attributeName"] == "resourceName"):
					global container_name
					container_name = item["attributeValue"]
					container_name_list.append(container_name)
				if (item["attributeName"] == "parentID"):
					a = len(item["attributeValue"].split('/'))
					container_parent = item["attributeValue"].split('/')[a-1]
					if container_parent == AE_name:
						source_id = AE_id
						target_id = container_id
			x_container = x_container + round(random.uniform(500,600),3)
			global edge_id
			edge_id += 1
			edge_string = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(source_id, target_id, edge_id)
			edge_string_list.append(edge_string)		
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"resourceType\":\"%s\",\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":8.5},' %(container_id, container_name, resourceType,x_container ,y_container)
			node_string_list.append(node_string)
		if resourceType == 'contentInstance(latest-allAttributes)':
			attributes = input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					CI_id = item["attributeValue"]
				if (item["attributeName"] == "resourceName"):
					CI_name = item["attributeValue"]
				if (item["attributeName"] == "parentID"):
					a = len(item["attributeValue"].split('/'))
					CI_parent = item["attributeValue"].split('/')[a-1]
					print 'CI_parent is...'
					print CI_parent 
					for index, containername in enumerate(container_name_list):
						if CI_parent == containername:
							source_id = container_id_list[index]
							target_id = CI_id
					print 'this is CI_id'
					print target_id
					print 'this is container_id'
					print source_id
			x_CI = x_CI + round(random.uniform(500,600),3)
			edge_id += 1
			edge_string = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(source_id, target_id, edge_id)
			edge_string_list.append(edge_string)
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"resourceType\":\"%s\",\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":8.5},' %(CI_id, CI_name, resourceType,x_CI ,y_CI)
			node_string_list.append(node_string)
				

GetContainerAttributes()
GetCIAttributes()
for string in attributes_output_list:
	Generate_json_string(string)
for string in node_string_list:
	all_node_string += string
	if (string == node_string_list[-1]):
		all_node_string = all_node_string[:len(all_node_string)-1]
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
parsed = json.loads(json_string)
pretty_json_string = json.dumps(parsed, indent=4, sort_keys=True)
text_file = open("test.json", "w")
text_file.write(pretty_json_string)
text_file.close()
print 'Json has been successfully created'

end_time = time.time()
print end_time - start_time

