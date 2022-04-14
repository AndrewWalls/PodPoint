import json
import http.client
import re
import datetime

#Gets the current date and time

now = datetime.datetime.now()
currentHour = int(now.hour)
currentMinute = int(now.minute+1)
currentSecond = int(now.second)

# Place your PodPoint Username below
username = "email@domain.com"

# Place your PodPoint Password below
podpointPassword = "Password1"

# Place your EV's usable battery size below in kWh (just as a number) 45kWh has been written below
evcapacity = int(45)

# Calculates the seconds required to raise your battery by 1%
percentageSeconds = float((evcapacity/100)*544.4444444444444444)

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


# Gets Charge State and Calculates Best Charge

from urllib import request
import datetime
battery = input("Please Enter the current battery level as a number (no percentage sign): ")
chargelevel = input("Please enter the desired charge level as a number (no percentage sign): ")
battery = int(battery)
chargelevel = int(chargelevel)
chargerequired = int(chargelevel - battery)
if chargerequired > 0:
    charge = chargerequired*percentageSeconds
    charge = round(charge)
    charge = int(charge)
    charge = charge+90
    starttime = datetime.datetime(100,1,1,0,30,0)
    stoptime = starttime + datetime.timedelta(0,charge) # days, seconds, then other fields.
    starttime = str(starttime)
    starttime = starttime[11:]
    stoptime = str(stoptime)
    stoptime = stoptime[11:]
    print(starttime)
    print(stoptime)
else:
    battery = str(battery)
    print("Battery at "+battery+"%")
    battery = int(battery)
    starttime = "00:00:00"
    stoptime = "00:00:01"
    print(starttime)
    print(stoptime)

chargestate = True

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