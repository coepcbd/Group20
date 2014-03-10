import os
import json
from glanceclient import Client

def get_id(url, tenant_name, username, password):
	syscall = "curl  'http://" + url + ":5000/v2.0/tokens' -X POST -H \"Content-Type: application/json\" -H \"Accept: application/json\" -H \"User-Agent: python-novaclient\" -d '{\"auth\": {\"tenantName\": \"" + tenant_name + "\", \"passwordCredentials\": {\"username\": \"" + username + "\", \"password\": \"" + password + "\"}}}' > response.txt"
	print syscall
	os.system(syscall)
 
	json_data = open("response.txt")

	data = json.load(json_data)

	json_data.close()
	return data['access']['token']['id']


option = 0

token_id = ""
image_name=""
while option != 6:
	print "1. Get Id\n 2. Create Image\n 3. Update image\n 4. Display list\n 5. Delete image\n 6. Exit\n Enter choice:\n "
	option = int(raw_input()) 

	if option == 1:
		print "Enter ip, tenant_name, username, password"
		url = raw_input()
		tenant_name = raw_input()
		username = raw_input()
		password = raw_input()
		token_id = get_id(url, tenant_name, username, password)
		glance = Client('1', endpoint="http://"+url+":9292",token=token_id)
	elif option == 2:
		if token_id == "":
			print "First Get id"
			break
		else:
			print "Enter Image name"
			image_name = raw_input()		
			new_image = glance.images.create(name=image_name)
			print "Image is " + new_image.status
	elif option == 3:
		if image_name=="":
			print "First create Image"
			break	
		else :
			print "Enter Image Path, format"
			image_path=raw_input()
			image_format=raw_input()
			new_image.update(data=open(image_path,'rb'),disk_format=image_format,name=image_name)
	elif option == 4:
		print "List of Images is "
		os.system("glance image-list")
	elif option == 5:
		os.system("glance image-list")
		print "Enter image id from above list to delete"
		del_img_id = raw_input()
		glance.images.delete(del_img_id)
		os.system("glance image-list")
	elif option == 6:
		break
