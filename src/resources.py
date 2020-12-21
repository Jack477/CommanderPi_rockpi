import os
import subprocess as sp
import fileinput
import configparser
import psutil
import platform
from os import path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

home_path = sys.argv[1]

### create config file
config = configparser.ConfigParser()
if os.path.exists(home_path+'/CommanderPi/src/cpi.config'):
	config.read(home_path+'/CommanderPi/src/cpi.config')
	print("Exist and read")
else:
	print("Creating config...")
	config['DEFAULT'] = {'color_mode': '0',
	'version': '0.4.2'}
	with open(home_path+'/CommanderPi/src/cpi.config', 'w') as configfile:
		config.write(configfile)

### update stuff
app_version = "Version 0.7armbian\n"
print("Here is app-1 "+app_version[:-1])
def get_app_version():
	return app_version



### network data

network = psutil.net_if_addrs()
ipv4eth = network['eth0'][0][1]
ipv6eth = None
maceth = network['eth0'][0][2]
try:
	ipv6eth = network['eth0'][1][1]
	maceth = network['eth0'][2][1]
except IndexError:
	ipv6eth = None
	ipv4eth = None
	maceth = network['eth0'][0][1]

broadcasteth = network['eth0'][0][3]

eth0_data = "IPv4 "+str(ipv4eth)+"\nIPv6 "+str(ipv6eth)+"\nMAC "+str(maceth)+"\nBroadcast "+str(broadcasteth)

ipv4wlan0 = network['wlan0'][0][1]
ipv6wlan0 = None
try:
	ipv6wlan0 = network['wlan0'][1][1]
	macwlan0 = network['wlan0'][2][1]
except IndexError:
	ipv6wlan0 = None
	ipv4wlan0 = None
	macwlan0 = network['wlan0'][0][1]
broadcastwlan = network['wlan0'][0][3]


wlan0_data = "IPv4 "+str(ipv4wlan0)+"\nIPv6 "+str(ipv6wlan0)+"\nMAC "+str(macwlan0)+"\nBroadcast "+str(broadcastwlan)

def get_country_code():
	country_code = sp.getoutput('iw reg get')
	country_code = country_code.splitlines()
	xcountry_code = ''
	for line in country_code:
		if "country" in line:
			xcountry_code = line
	xcountry_code = xcountry_code[8:10]
	if(xcountry_code=='00'):
		return "None"
	else:
		return xcountry_code

print("Country code is:")
print(get_country_code())

### set country code
def set_country_code(code):
	path = "/etc/default/crda"
	xcode = ""
	with open(path) as f:
		for line in f:
			if "REGDOMAIN=" in line:
				xcode = line
	print(xcode)
	fin = open(path, "rt")
	data = fin.read()
	data = data.replace(xcode, 'REGDOMAIN='+str(code))
	fin.close()
	fin = open(path, "wt")
	fin.write(data)
	fin.close()
	os.system("sudo iw reg set "+code)



### DISK SPACE 
hdd = psutil.disk_usage('/')
def get_total_space():
	return hdd.total / (2**30)
def get_used_space():
	return hdd.used / (2**30)
def get_free_space():
	return hdd.free / (2**30)
def get_disk_percent():
	return hdd.percent

total = str(round(get_total_space(), 2))
used = str(round(get_used_space(), 2))
free = str(round(get_free_space(),2))
disk = str(get_disk_percent())
print (hdd.percent)
print ("Total: " + total)
print ("Used: " + used)
print ("Free: " + free)


#### Check entry in gui (overclocking) is preesed
push_state1 = False
push_state2 = False
push_state3 = False
def set_push_state(state):
	global push_state1
	global push_state2
	global push_state3
	if ( state == 1 ):
		push_state1 = True
	elif ( state == 2):
		push_state2 = True
	elif (state == 3):
		push_state3 = True

### get cpu informations

def getproc0():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 1 | sed -e s/$/:/')
	cpux = str(cpu)
	return cpux
	
def getproc1():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 2 | sed -e s/^[[:space:]]*//')
	cpux = str(cpu)
	return cpux

### reboot RPI	
def reboot():
	os.system("sudo reboot now")
	
### get cpu usage in MHz & GHz
def refusage():
	cpu_freq = psutil.cpu_freq()
	buff = cpu_freq[0]
	return str(buff)+" MHz"

### get gpu usage in MHz & GHz
def refgpu():
	gpu_usagex = sp.getoutput('cat /sys/class/drm/card1/device/devfreq/ff9a0000.gpu/cur_freq | cut -c1-3')
	return gpu_usagex+" MHz"


### get ram usage
def refmem():
	memory_usex = psutil.virtual_memory().percent
	memory_use = str(memory_usex)
	return memory_use

### get cpu temperature
def reftemp():
	temp = psutil.sensors_temperatures()
	temp = round(temp['cpu'][0][1])
	return str(temp)+"'C"

### get gpu temperature
	
def reftemp2():
	temp = psutil.sensors_temperatures()
	temp = round(temp['gpu'][0][1])
	return str(temp)+"'C"	
	
	
	### BOARD VERSION ###
board_versionx = sp.getoutput('cat /proc/device-tree/model')
board_version = board_versionx[:-1]

def get_board_version():
	if "ROCK Pi" in board_version:
		return board_version
	if "Pi 3 Model B Plus" in board_version:
		return 3
	if "Pi 4 Model" in board_version:
		return 4
		

	
processor_architecture = platform.machine()
kernel_version = platform.release()



config_path=""
if path.exists("/boot/config.txt"):
	config_path = "/boot/config.txt"
elif path.exists("/boot/firmware/usercfg.txt"):
	config_path = "/boot/firmware/usercfg.txt"
elif path.exists("/media/pi/boot/config.txt"):
	config_path = "/media/pi/boot/config.txt"
else:
	print("Can't find RaspberryPi config file!")


def get_kernel_mode():
	if "arm_64bit=1" in arm_64bit:
		return "64bit"
	else:
		return "32bit"



