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

# Set the threshold for pence per kWh for your PodPoint to activate. 7.22p has been set below as an example
agileThreshold = float(7.22)

loop = 1

while loop == 1:

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


    # Calculates how many seconds it is to the next half hour or hour (whichever is soonest) and sets this as the varibale delayTimer. This will be used to poll the current Agile rate on the half hour

    now = datetime.now()
    minutes = now.strftime("%M")
    seconds = now.strftime("%S")
    minutes = int(minutes)
    seconds = int(seconds)
    minutes = minutes*60
    currentTime = (minutes+seconds)

    if currentTime < 1800:
        delayTimer = (1800-currentTime)
    else:
        delayTimer = (3600-currentTime)

    #Uses the current time to get the current Octopus Agile rate using the Octopus Agile API

    currentDay = now.strftime("%d")
    currentMonth = now.strftime("%m")
    currentYear = now.strftime("%Y")
    currentHour = now.strftime("%H")
    currentMinute = now.strftime("%M")
    currentSecond = now.strftime("%S")
    r = request.urlopen("https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-J/standard-unit-rates/?period_from="+currentYear+"-"+currentMonth+"-"+currentDay+"T"+currentHour+":"+currentMinute+":"+currentSecond+"&period_to="+currentYear+"-"+currentMonth+"-"+currentDay+"T"+currentHour+":"+currentMinute+":"+currentSecond+".1")
    bytecode = r.read()
    htmlstr = bytecode.decode()
    bytecode = str(bytecode)
    agilePrice = re.search(r'inc_vat\":(.*?),', bytecode).group(1)
    agilePrice = str(agilePrice)
    print(""+currentHour+":"+currentMinute+":"+currentSecond+"")
    print("The current rate is "+agilePrice+"p per kWh.")
    agilePrice = float(agilePrice)
    if agilePrice < agileThreshold:
        print("Activating PodPoint Charger")
        chargestate = False
    else:
        print("Deactivating PodPoint Charger")
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
    time.sleep(delayTimer)