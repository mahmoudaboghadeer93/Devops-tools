import requests
 
url = "https://tscloud.x.com/api/v1/applications/new"
 
headers = {
    'Authorization': "Bearer Token_key",
}
 
app = open('demo2.apk','rb')
files = {'file': app}
 
response=requests.post(url, files=files, headers=headers)
jsonresponse=response.json()
print(jsonresponse["data"])

app_id=jsonresponse["data"]

install_url = "https://tscloud.x.com/api/v1/applications/%s/install" %app_id

install_params = { "AllDevices" : "true" }

install_response=requests.post(install_url,params=install_params,headers=headers)
	
print(install_response.content)
