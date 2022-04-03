# PodPoint
Scripts that can be used to enhance the functionality of domestic PodPoint EV Chargers using the PodPoint APIs. Please note this is a personal project and not officially linked to PodPoint as a company.

#LowCarbonPodPoint.py

In this file you need to replace the values at the top with your username, password and the maximum threshold of grams of CO2 per kWh that you wish your charger to turn on at. The script needs to be left running, ideally on a low power device such as a RaspberryPi.

#LockUnlockCharger.py

On line 9 enter your PodPoint username over the placeholder. On line 12 enter your PodPoint password over the placeholder.
When you run the script you can enter either 1 to lock the PodPoint charger. This will set the PodPoint to activate for just one second at midnight each day. As this is not enough time to power up the PodPoint it will remain offline and therefore locked. If you press 2 it will reset all timers and be constantly on.

#OctopusAgile.py

On line 9 enter your PodPoint username over the placeholder. On line 12 enter your PodPoint password over the placeholder. On line 15, inside the brackets, set the threshold in pence per kWh on the Octopus Agile tarrif when your PodPoint will activate. If you entered 8 or 7.22 as soon as the price falls below this value your PodPoint will turn on. If it goes above this price then the PodPoint will turn off. The script needs to be left running, ideally on a low power device such as a RaspberryPi. If you close the script, the PodPoint will remain in its current state of being either fully on or fully off.

#OctopusGo.py

On line 9 enter your PodPoint username over the placeholder. On line 12 enter your PodPoint password over the placeholder. When the script runs it will set your PodPoint for all days to the lower cost 7.5p overnight OctopusGo hours of 00:30:00 to 04:30:00.
