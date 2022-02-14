import ConfigParser
import inspect
import os
import wordclock_tools.wordclock_display as wcd
import wordclock_interfaces.event_handler as wci
import time

basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pathToConfigFile = basePath + '/wordclock_config/wordclock_config.cfg'
config = ConfigParser.ConfigParser()
config.read(pathToConfigFile)

config.set('wordclock', 'base_path', basePath)
wci = wci.event_handler()

wcd = wcd.wordclock_display(config, wci)

wcd.setImage(basePath + "/wordclock_plugins/restart/icons/11x10/logo.png")


flag_file = basePath + "/boot_config.flag"
if os.path.isfile(flag_file):
    os.remove(flag_file)
