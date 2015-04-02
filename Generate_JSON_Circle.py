import json
import requests
import time
import random
import pdb
import math

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
CI_count = 0
all_node_string = ''
all_edge_string = ''
json_string = ''
AE_url = 'http://54.68.184.172:8282/InCSE1/Team2AEx'


r = requests.get(AE_url,params=Parameter2,headers = Header)
output_AE_2 = r.text
s = requests.get(AE_url,params=Parameter10,headers = Header)
output_AE_10 = s.text
attributes_output_list.append(output_AE_10)

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
	global CI_count
	container_name_list = GetChildList(output_AE_2, 'child-container List')
	for name in container_name_list:
		Container_URL = AE_url + '/%s' %(name)
		r = requests.get(Container_URL, params = Parameter2, headers = Header)
		output_for_container = r.text
		ci_name_list = GetChildList(output_for_container, 'child-contentInstance List')
		for CI_Name in ci_name_list:
			CI_count += 1
			CI_URL = Container_URL + '/%s' %(CI_Name)
			r = requests.get(CI_URL, params = Parameter10,headers = Header)
			output_for_CI = r.text
			attributes_output_list.append(output_for_CI)

def GetContainerAttributes():
	global container_count
	container_name_list = GetChildList(output_AE_2, 'child-container List')
	for name in container_name_list:
		container_count += 1
		Container_URL = AE_url + '/%s' %(name)
		r = requests.get(Container_URL, params = Parameter10, headers = Header)
		output_for_container = r.text
		attributes_output_list.append(output_for_container)

def Generate_json_string(input_json_string):
	global x_AE, y_AE, x_container, y_container, x_CI, y_CI, theta_container, theta_CI
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
				if (item["attributeName"] == "labels"):
					AE_labels = item["attributeValue"]
				if (item["attributeName"] == "parentID"):
					AE_parent = item["attributeValue"]
				if (item["attributeName"] == "Total Child Resource Number"):
					AE_child_num = item["attributeValue"]
				if (item["attributeName"] == "Child-ResourceContainer Number"):
					AE_child_container_num = item["attributeValue"]
				if (item["attributeName"] == "Child-ResourceSubscription Number"):
					AE_child_sub_num = item["attributeValue"]
			
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"attributes\":{\"resourceID\":\"%s\",\"resourceType\":\"%s\",\"labels\":\"%s\",\"parentID\":\"%s\",\"Total Child Resource Number\":\"%s\",\"Child-ResourceContainer\":\"%s\",\"Child-ResourceSubscription Number\":\"%s\"},\"x\":%s,\"y\":%s,\"color\":\"rgb(255,204,102)\",\"size\":15},' %(AE_id, AE_name, AE_id, resourceType, AE_labels, AE_parent, AE_child_num, AE_child_container_num, AE_child_sub_num, x_AE, y_AE)
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
				if (item["attributeName"] == "labels"):
					container_labels = item["attributeValue"]
				if (item["attributeName"] == "parentID"):
					container_parent_id = item["attributeValue"]
					a = len(item["attributeValue"].split('/'))
					container_parent = item["attributeValue"].split('/')[a-1]
					if container_parent == AE_name:
						source_id = AE_id
						target_id = container_id
				if (item["attributeName"] == "stateTag"):
					container_stateTag = item["attributeValue"]
				if (item["attributeName"] == "currentByteSize"):
					container_cur_size = item["attributeValue"]
				if (item["attributeName"] == "currentNrofInstance"):
					container_count_cur_ins = item["attributeValue"]
				if (item["attributeName"] == "Total Child Resource Number"):
					container_child_num = item["attributeValue"]
					container_node_size = 1
					container_node_size = container_node_size * container_child_num
				if (item["attributeName"] == "Child-ResourceContainer Number"):
					container_child_container_num = item["attributeValue"]
				if (item["attributeName"] == "Child-ResourceContentInstance Number"):
					container_child_CI_num = item["attributeValue"]
				if (item["attributeName"] == "Child-ResourceSubscription Number"):
					container_child_sub_num = item["attributeValue"]
			r = 2000
			theta_container = theta_container + 360 / container_count
			print theta_container
			x_container = x_AE + r * math.cos(theta_container)
			y_container = y_AE + r * math.sin(theta_container)
			global edge_id
			edge_id += 1
			edge_string = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(source_id, target_id, edge_id)
			edge_string_list.append(edge_string)		
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"attributes\":{\"resourceID\":\"%s\",\"resourceType\":\"%s\",\"labels\":\"%s\",\"parentID\":\"%s\",\"stateTag\":\"%s\",\"Total Child Resource Number\":\"%s\",\"Child-ResourceContainer\":\"%s\",\"Child-ResourceContentInstance Number\":\"%s\",\"Child-ResourceSubscription Number\":\"%s\"},\"x\":%s,\"y\":%s,\"color\":\"#36e236\",\"size\":%s},' %(container_id, container_name, container_id, resourceType, container_labels, container_parent_id, container_stateTag, container_child_num, container_child_container_num, container_child_CI_num, container_child_sub_num, x_container ,y_container, container_node_size)
			node_string_list.append(node_string)
		if resourceType == 'contentInstance(latest-allAttributes)':
			attributes = input_json_string["ResourceOutput"][0]["Attributes"]
			for item in attributes:
				if (item["attributeName"] == "resourceID"):
					CI_id = item["attributeValue"]
				if (item["attributeName"] == "resourceName"):
					CI_name = item["attributeValue"]
					container_labels = item["attributeValue"]
				CI_resourceType = 'contentInstance'
				if (item["attributeName"] == "creationTime"):
					CI_creation_time = item["attributeValue"]
				if (item["attributeName"] == "lastModifiedTime"):
					CI_modified_time = item["attributeValue"]
				if (item["attributeName"] == "labels"):
					CI_labels = item["attributeValue"]
				if (item["attributeName"] == "parentID"):
					CI_parent_id = item["attributeValue"]
					a = len(item["attributeValue"].split('/'))
					CI_parent = item["attributeValue"].split('/')[a-1]
					#print 'CI_parent is...'
					#print CI_parent
					for index, containername in enumerate(container_name_list):
						if CI_parent == containername:
							source_id = container_id_list[index]
							target_id = CI_id
					#print 'this is CI_id'
					#print target_id
					#print 'this is container_id'
					#print source_id
				if (item["attributeName"] == "stateTag"):
					CI_stateTag = item["attributeValue"]
			r = 4000
			theta_CI = theta_CI + 360 / CI_count
			print theta_CI
			x_CI = x_AE + r * math.cos(theta_CI)
			y_CI = y_AE + r * math.sin(theta_CI)
			edge_id += 1
			edge_string = '{\"source\":\"%s\",\"target\":\"%s\",\"id\":\"%s\"},' %(source_id, target_id, edge_id)
			edge_string_list.append(edge_string)
			node_string = '{\"id\":\"%s\",\"label\":\"%s\",\"attributes\":{\"resourceID\":\"%s\",\"resourceType\":\"%s\",\"creationTime\":\"%s\",\"lastModifiedTime\":\"%s\",\"labels\":\"%s\",\"parentID\":\"%s\",\"stateTag\":\"%s\"},\"x\":%s,\"y\":%s,\"color\":\"#3636e2\",\"size\":0.5},' %(CI_id, CI_name, CI_id, CI_resourceType, CI_creation_time, CI_modified_time, CI_labels, CI_parent, CI_stateTag, x_CI ,y_CI)
			node_string_list.append(node_string)
				
GetContainerAttributes()
GetCIAttributes()
print container_count
print CI_count
edge_id = 0
x_AE = 0
y_AE = 0
theta_container = 0
theta_CI = 0
#if (container_count % 2 == 0):
#	y_container= container_count / 2 * (-500) - 500
#else:
#	y_container = (container_count - 1) / 2 * (-500) - 500
#x_container = 2000
if (CI_count % 2 == 0):
	y_CI = CI_count / 2 * (-500) -500 
else:
	y_CI = (CI_count - 1) / 2 * (-500) -500
x_CI = 4000
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
#print all_node_string
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
#print all_edge_string
print '----------------------------'
json_string = all_edge_string + all_node_string
parsed = json.loads(json_string)
pretty_json_string = json.dumps(parsed, indent=4, sort_keys=True)
text_file = open("/Users/FinleyZhu/Desktop/iot-ui-bigdata/network/data/iot.json", "w")
text_file.write(pretty_json_string)
text_file.close()
print 'iot.json has been successfully created'

end_time = time.time()
print end_time - start_time

