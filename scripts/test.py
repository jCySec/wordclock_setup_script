from configparser import ConfigParser
from inspect import currentframe
from inspect import getfile
from os.path import dirname
from os.path import abspath
from os.path import isfile
from os.path import join as joinpath
from os import system
from os import remove
from datetime import datetime
from sys import executable
from time import sleep
from subprocess import check_output
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
import wordclock_tools.wordclock_display as wcd
import wordclock_interfaces.event_handler as wci


def reset_mode(flag_file, wcd, basePath):
	# Set the flag_file to True
	# remove(flag_file)
	print("Set flag to True")
	with open(flag_file, "w+", buffering=1) as f:
		f.seek(0)
		n = f.write("True")	
		f.truncate()
		f.flush()
		f.close()

	# Show bolt
	bolt_icon = joinpath(basePath, "icons/11x10/boot_reset_bolt.png")
	wcd.setImage(bolt_icon)
	# Wait 10s to allow the user to cut the power!
	# If power is cut during these 10s the wordclock should boot into config mode since the flag is still set to True!
	sleep(20)
	wcd.resetDisplay()
	wcd.show()
	# Okay, 10s are over => user does not want to configure his wifi so remove the flag!
	# remove(flag_file)
	print("Set Flag back to False!")
	with open(flag_file, "w+", buffering=1) as f:
		f.seek(0)
		n = f.write("False")
		f.truncate()
		f.flush()
		f.close()
	
	return True


def check_wifi_connection():
	wifi_state = False
	for i in range(6):
		iwconfig_out = check_output(['iwconfig']).decode('utf-8')
		if "Access Point: Not-Associated" in iwconfig_out:
			# Wifi not active
			# => sleep and continue
			sleep(10)
			continue
		else:
			# Wifi is already active
			# => set True and leave here
			wifi_state = True
			break
	return wifi_state


if __name__ == "__main__":
	# load wordclock interface
	basePath = dirname(abspath(getfile(currentframe())))
	pathToConfigFile = joinpath(basePath, 'wordclock_config/wordclock_config.cfg')
	config = ConfigParser()
	config.read(pathToConfigFile)

	config.set('wordclock', 'base_path', basePath)
	wci = wci.event_handler()

	wcd = wcd.wordclock_display(config, wci)

	## check for Flag file
	# join path for boot_config.flag file
	flag_file = joinpath(basePath, "boot_config.flag")
	# check if flag_file exists and create if not available with default False value
	if not isfile(flag_file):
		with open(flag_file, "w+") as f:
			n = f.write("False")
			f.flush()
			f.close()
	
	# Check flag_file value:
	with open(flag_file, "r") as f:
		flag_value = f.readline()
		f.close()
	
	print("Flag Value: {}".format(flag_value))
	if flag_value == "True":
		# If True => trigger boot into config mode!
		print("Flag is True!")
	else:
		reset_mode(flag_file, wcd, basePath)

