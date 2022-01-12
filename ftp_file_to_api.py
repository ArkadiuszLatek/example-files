import sys
import requests
import json
import os
from ftplib import FTP

tAuth = os.environ.get('file1')

with open(tAuth, "r") as read_file:
    data = json.load(read_file)
    apiUser = str(data['p']['User'])
    apiPass = str(data['p']['Passw'])

#download last file
ftp = FTP(updaterHost)
ftp.login(user=updaterUser, passwd=updaterPassword)
print("Logged to clients ftp successfully")
sys.stdout.flush()

# In lines below I'm using MDTM command to retrieve timestamps of individual files/folders:
names = ftp.nlst()
latest_time = None
latest_name = None

for name in names:
    myfile = ftp.voidcmd("MDTM " + name)
    if (latest_time is None) or (myfile > latest_time):
        latest_name = name
        latest_time = myfile

file = open(latest_name, 'wb')
print("File download in progress...")
ftp.retrbinary('RETR '+ latest_name, file.write)

ftp.quit()
print("File downloaded")
sys.stdout.flush()

passy = (apiUser, apiPass)
finalJson = {'FixingRules':[]}

Endpoint = 'https://api.biz/api/client'

print("Latest file name is: {}".format(latest_name))

file = open(latest_name, 'r')
next(file)
lines = file.readlines()

for line in lines:
    convType = line.strip().split(";")[0].replace(' ', '_').upper()
    convPatt = line.strip().split(";")[1]
    cpa = line.strip().split(";")[2]
    cps = line.strip().split(";")[3]
    if cpa == '':
        cpa = 0
        cps = float(cps.replace('%', '').replace(',', '.'))/100
    if cps == '':
        cps = 0
        cpa = float(cpa.replace(',', '.'))

    finalJson['FixingRules'].append({"cType": "{}".format(convType), "cPattern": "{}".format(convPatt), "cps": cps, "cpa":cpa})

res = requests.get(Endpoint, auth=passy)
jsone = res.json()
print(jsone)
url = '{}?version={}'.format(Endpoint, jsone['data']['version'])

print(url)
puter = requests.put(url, json=finalJson, auth=passy)
print(puter.text)
