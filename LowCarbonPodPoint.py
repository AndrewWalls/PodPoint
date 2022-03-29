import re
import http.client
import json
import time
from urllib import request
from datetime import datetime

# Place your PodPoint Username below
username = "email@domain.com"

# Place your PodPoint Password below
podpointPassword = "Password1"

# Place your postcode below as a single lowercase string with no spaces. For example B83 1JH would be b831jh
postcode = "b901aa"

# Set the threshold for CO2 emissions per kWh below
carbonthreshold = 100

# Authenticates and gets an access token from PodPoint

conn = http.client.HTTPSConnection("api.pod-point.com")
payload = json.dumps({
  "username": username,
  "password": podpointPassword
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/v4/auth", payload, headers)
res = conn.getresponse()
data = res.read()
data = (data.decode("utf-8"))
access_token = re.search(r'\"access_token\": \"(.*?)\",', data).group(1)
access_token = "Bearer "+access_token+""

# Gets your PodPoint UserID

conn = http.client.HTTPSConnection("api.pod-point.com")
payload = 'account'
headers = {
  'Authorization': access_token
}
conn.request("GET", "/v4/auth", payload, headers)
res3 = conn.getresponse()
data3 = res3.read()
data3 = str(data3)
idvalue = re.search(r'\"id\": (.*?),', data3).group(1)

# Gets the name of your PodPoint Charger

conn = http.client.HTTPSConnection("api.pod-point.com")
payload = ''
headers = {
  'Authorization': access_token
}
conn.request("GET", "/v4/users/"+idvalue+"/pods?perpage=all&include=statuses,price,model,unit_connectors,charge_schedules", payload, headers)
res2 = conn.getresponse()
data2 = res2.read()
data2 = str(data2)
unitid = re.search(r'\"unit_id\": (.*?),', data2).group(1)
unitid = str(unitid)

#Sets your PodPoint timer to come on for one second each day with the below variables. This would constitute it being "off".

starttime = "00:00:00"
stoptime = "00:00:01"

x = True

# Loop to get CO2 readings every minute from your local substation and to decide whether your PodPoint should be on or off

while x == True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

    # Gets UUID of your local substation

    r = request.urlopen("https://carbontracer.westernpower.co.uk/carbonapi/get_bsp_by_postcode/" +postcode+"")
    bytecode2 = r.read()
    htmlstr2 = bytecode2.decode()
    bytecode2 = str(bytecode2)
    substationid = re.search(r'id\":(.*?),', bytecode2).group(1)

    # Gets Current CO2 from WPD for your local substation

    r = request.urlopen("https://carbontracer.westernpower.co.uk/carbonapi/get_carbon_intensity_now/" +substationid+"")
    bytecode = r.read()
    htmlstr = bytecode.decode()
    bytecode = str(bytecode)
    carbon = re.search(r'{\"data\":(.*?)}', bytecode).group(1)
    carbon = float(carbon)

    # Sets charge state to True or False if the carbon is below the carbon threshold


    if carbon < carbonthreshold:
        chargestate = False
        carbon = str(carbon)
        print("Charger is online. Current carbon emissions are "+carbon+"g per kWh.")
        carbon = float(carbon)
    else:
        chargestate = True
        carbon = str(carbon)
        print("Charger is offline. Current carbon emissions are "+carbon+"g per kWh.")
        carbon = float(carbon)
    conn = http.client.HTTPSConnection("api.pod-point.com")
    payload = json.dumps({
    "data": [
        {
          "start_day": 1,
          "start_time": starttime,
          "end_day": 1,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 2,
          "start_time": starttime,
          "end_day": 2,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 3,
        "start_time": starttime,
        "end_day": 3,
        "end_time": stoptime,
        "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 4,
          "start_time": starttime,
          "end_day": 4,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 5,
          "start_time": starttime,
          "end_day": 5,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 6,
          "start_time": starttime,
          "end_day": 6,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        },
        {
          "start_day": 7,
          "start_time": starttime,
          "end_day": 7,
          "end_time": stoptime,
          "status": {
            "is_active": chargestate
          }
        }
    ]
    })
    headers = {
    'Authorization': access_token,
    'Content-Type': 'application/json'
    }
    conn.request("PUT", "/v4/units/"+unitid+"/charge-schedules", payload, headers)
    res = conn.getresponse()
    data = res.read()
    time.sleep(60)