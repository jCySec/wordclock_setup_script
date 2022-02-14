import os
import time

class plugin:
	"""
	A class to reset the wordclock into wifi config mode!
	"""

	def __init__(self, config):
		self.name = os.path.dirname(__file__).split('/')[-1]
		self.pretty_name = "Reboot into Wifi Config"
		self.description = "Forget your wifi and reboot into Wifi Config mode!"

	def run(self, wcd, wci):
		wcd.showText("reboot into wifi config...")
		wcd.showIcon(plugin=self.name, iconName="logo")
		os.system("/usr/bin/python3 /usr/lib/raspiwifi/reset_device/manual_reset.py")
		time.sleep(10)
		return
