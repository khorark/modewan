#!/usr/bin/env python3
#
#  modewan.py
#  
#  Copyright 2015 Khorark
#  Version 0.1 
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import os, sys
import subprocess
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def monitor_mode(num):
	mac_new = input ('Change the MAC interface wlan{} y/n\n'.format(num))
	if mac_new == 'y':
		subprocess.call("ifconfig wlan{} down".format(num), shell=True)
		subprocess.call('macchanger -r wlan{}'.format(num), shell=True)
		subprocess.call("iwconfig wlan{} mode monitor".format(num), shell=True)
		subprocess.call("ifconfig wlan{} up".format(num), shell=True)
		print ('MAC change. {}Monitor mode{} in enable for wlan{}'.format(bcolors.WARNING,bcolors.ENDC,num))
		
	if mac_new == 'n':
		subprocess.call("ifconfig wlan{} down".format(num), shell=True)
		subprocess.call("iwconfig wlan{} mode monitor".format(num), shell=True)
		subprocess.call("ifconfig wlan{} up".format(num), shell=True)
		print ('{}Monitor mode{} in enable for wlan{}'.format(bcolors.WARNING,bcolors.ENDC,num))
		
def manage_mode(num):
	subprocess.call("ifconfig wlan{} down".format(num), shell=True)
	subprocess.call("iwconfig wlan{} mode managed".format(num), shell=True)
	subprocess.call("ifconfig wlan{} up".format(num), shell=True)
	print ('{}Managed mode{} in enable for wlan{}'.format(bcolors.WARNING,bcolors.ENDC,num))

def main():

	if not os.geteuid() == 0:
		sys.exit(bcolors.FAIL + "\nOnly root can run this script\n" + bcolors.ENDC)
		
	#выполняем команду 'ifconfig' и записываем результат
	output = str(subprocess.check_output("ifconfig"))
	num = (len(re.findall('wlan', output)))

	while True:
		try:
			print ('Select interface')
			dict_wlan = {}
			for x in range(0,num):
				mode = str(subprocess.check_output("iwconfig wlan{}".format(x), shell=True))
				if mode.find('Monitor') != -1:
					mode = mode[mode.find('Monitor'):mode.find('Monitor') + 7]
					color_text = bcolors.OKBLUE
				if mode.find('Managed') != -1:
					mode = mode[mode.find('Managed'):mode.find('Managed') + 7]
					color_text = bcolors.OKGREEN 
				print ('{}) wlan{}    -    Mode: {}{}{}'.format(x+1,x,color_text,mode,bcolors.ENDC))
				dict_wlan[x] = mode
			
			sel_wlan = int(input()) - 1
			
			if sel_wlan >= num or sel_wlan < 0:
				print ('This interface is not found')
				break

			if dict_wlan[sel_wlan] == 'Managed':	
				monitor_mode(sel_wlan)				
				exit(0)
					
			if dict_wlan[sel_wlan] == 'Monitor':
				manage_mode(sel_wlan)
				exit(0)	
				
		except ValueError:
			print('This is not digital.')
	return 0
			
if __name__ == '__main__':
    main()
