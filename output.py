output = '{"output":{"responseStatusCode":2002,"ResourceOutput":[{"resourceType":"AE","resourceID":"1415208429","Attributes":[{"attributeName":"child-container List","attributeValue":"[InCSE1/Team2AEx/container4, InCSE1/Team2AEx/container3, InCSE1/Team2AEx/container2, InCSE1/Team2AEx/container1, InCSE1/Team2AEx/container0, InCSE1/Team2AEx/container5, InCSE1/Team2AEx/container6, InCSE1/Team2AEx/container7, InCSE1/Team2AEx/container8, InCSE1/Team2AEx/container9]"}]}]}}'

def strip_off_name( output, first_keyword, last_keyword ):
			AE_name = '/Team2AEx/'
			#input the AE name here
			start_index = output.index(AE_name)
			remaining_string = output[start_index:]
			while True:
				try:
					start = remaining_string.index(first_keyword) + len(first_keyword)
					end = remaining_string.index(last_keyword)
					result = remaining_string[start:end]
					print result
					remaining_string_index = output.index(result) + len(result) + len(last_keyword)
					remaining_string = output[remaining_string_index:]
				except ValueError:
					#This is the process of getting the last container name 
					#Because the last remaining string is different in the normal while loop
					start = remaining_string.index( first_keyword ) + len( first_keyword )
					end = remaining_string.index( ']\"}' )
					result = remaining_string[start:end]
					print result
					print 'finish'
					break
			


strip_off_name(output, '/Team2AEx/', ', InCSE1')

