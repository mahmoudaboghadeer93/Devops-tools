import requests
import os
upload_url = "https://tscloud.x.com/api/v1/applications/new"

dir_path = r'upload'
# list to store files
res = []
# Iterate directory
for file in os.listdir(dir_path):
    appType = [".apk", ".ipa"]
    # check only text files
    if file.endswith(tuple(appType)):
        res.append(file)
print(res)
for x in range(len(res)):
    print(res[x])
app = open("upload/"+res[x],'rb')
files = {'file': app}
headers = {
    'Authorization': "Bearer "+os.getenv('AccessKey'),
}
response=requests.post(upload_url, files=files, headers=headers)
jsonresponse=response.json()
print(jsonresponse["data"])
app_id=jsonresponse["data"]
install_url = "https://tscloud.x.com/api/v1/applications/%s/install" %app_id
install_params = { "AllDevices" : "true" }
install_response=requests.post(install_url,params=install_params,headers=headers)
print(install_response.content)
