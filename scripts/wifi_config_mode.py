import configparser
import inspect
import os
import wordclock_tools.wordclock_display as wcd
import wordclock_interfaces.event_handler as wci
import time

basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pathToConfigFile = basePath + '/wordclock_config/wordclock_config.cfg'
config = configparser.ConfigParser()
config.read(pathToConfigFile)

config.set('wordclock', 'base_path', basePath)
wci = wci.event_handler()

wcd = wcd.wordclock_display(config, wci)

wcd.resetDisplay()
wcd.show()

time.sleep(1)
wcd.showText("WIFI CONFIG: 10.0.0.1", fps=10)
time.sleep(0.3)

for i in range(5):
	wcd.setImage(basePath + "/icons/11x10/wifi_0.png")
	time.sleep(0.7)
	wcd.setImage(basePath + "/icons/11x10/wifi_1.png")
	time.sleep(0.7)
	wcd.setImage(basePath + "/icons/11x10/wifi_2.png")
	time.sleep(0.7)
	wcd.setImage(basePath + "/icons/11x10/wifi_3.png")
	time.sleep(0.7)

wcd.setImage(basePath + "/icons/11x10/wifi_error.png")
