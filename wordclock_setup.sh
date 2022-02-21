#!/bin/bash

# Check for root-privileges
if [ "$(whoami)" != "root" ]; then
    echo -e "\n\e[34mThis script must be executed as root.\e[0m"
    echo -e "\e[34mAdd \"sudo\" in front of the command.\e[0m\n"
    exit 1
fi

# Check for internet connection
su pi -c "wget -q --spider http://google.com"
if [ $? -eq 0 ]; then
    echo "Internet connection confirmed."
else
    echo "No active internet connection detected - please ensure an active connection!"
    exit 1
fi

# Install 3rd party dependencies
echo -e "\e[34mInstalling 3rd party dependencies:\e[0m"
for pac in python3-pip python3-virtualenv python3-scipy scons git swig libopenjp2-7
do
   echo -e "\e[34m  Installing dependency $pac...\e[0m"
   sudo apt-get install -y $pac
   echo -e "\e[34m  Done.\e[0m"
done

# Create new venv with python3
echo -e "\e[34m\nCreate new virtualenviroment ...\e[0m"
su pi -c "virtualenv -p python3 /home/pi/wordclock/.PyEnvs"
echo -e "\e[34mDone.\e[0m"

# create folder for new wordclock version
echo -e "\e[34m\nCreate new wordclock project folder ...\e[0m"
su pi -c "mkdir /home/pi/wordclock"
echo -e "\e[34mDone.\e[0m"

# Activate the virtualenv
echo -e "\e[34m\nActivate virtualenv ...\e[0m"
su pi -c "source /home/pi/wordclock/.PyEnvs/bin/activate"
echo -e "\e[34mDone.\e[0m"

# Update pip
echo -e "\e[34m\nUpdate pip ...\e[0m"
su pi -c "/home/pi/wordclock/.PyEnvs/bin/python -m pip install --upgrade pip"
echo -e "\e[34mDone.\e[0m"

# Install 3rd party python dependencies
echo -e "\e[34m\nInstalling 3rd party python dependencies:\e[0m"
for pac in requests RPi.GPIO flask_restx ConfigParser pytz astral feedparser pillow svgwrite freetype-py netifaces monotonic flask-restplus coloredlogs rpi_ws281x
do
   echo -e "\e[34m  Installing python dependency $pac...\e[0m"
   su pi -c "/home/pi/wordclock/.PyEnvs/bin/pip install $pac"
   echo -e "\e[34m  Done.\e[0m"
done

# Install pywapi
echo -e "\e[34m\nInstalling pywapi\e[0m"
cd /home/pi/PyProjects/wordclock2022/
su pi -c "wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz"
su pi -c "tar -zxf pywapi-0.3.8.tar.gz"
rm pywapi-0.3.8.tar.gz
cd pywapi-0.3.8
su pi -c "/home/pi/wordclock/.PyEnvs/bin/python setup.py build"
su pi -c "/home/pi/wordclock/.PyEnvs/bin/python setup.py install"
echo -e "\e[34mDone.\e[0m"

# get the new wordclock software
echo -e "\e[34m\nInstalling new wordclock version\e[0m"
cd /home/pi/wordclock/
su pi -c "git clone https://github.com/bk1285/rpi_wordclock.git"
cd rpi_wordclock
su pi -c "git checkout --track origin/develop"
echo -e "\e[34mDone.\e[0m"

# Create adjustments for the wifi config mode
echo -e "\e[34m\nSync customization to wordclock setup ...\e[0m"
cd /home/pi/wordclock/
git clone https://github.com/jCySec/wordclock_setup_script.git
cp ./wordclock_setup_script/scripts/*.py ./rpi_wordclock/
cp ./wordclock_setup_script/icons/11x10/*.png ./rpi_wordclock/icons/11x10/
cp -r ./wordclock_setup_script/wordclock_plugins/* ./rpi_wordclock/wordclock_plugins/
echo -e "\e[34mDone.\e[0m"

# patch config
echo -e "\e[34m\nPull new default config:\e[0m"
cd /home/pi/wordclock/rpi_wordclock/wordclock_config/
su pi -c "wget https://raw.githubusercontent.com/jCySec/wordclock_setup_script/main/wordclock_config.cfg"
echo -e "\e[34mDone.\e[0m"

# patch the cron file
echo -e "\e[34m\nPatch the cron files...\e[0m"
# /home/pi/wordclock/.PyEnvs/bin/python /home/pi/PyProjects/wordclock2022/rpi_wordclock/boot_manager.py &
sed -i -e 's/wordclock/wordclock/g' /etc/cron.raspiwifi/apclient_bootstrapper
sed -i -e 's/rpi_wordclock/rpi_wordclock/g' /etc/cron.raspiwifi/apclient_bootstrapper
echo -e "\e[34mDone.\e[0m"

# Let's reboot
echo "\n\nREBOOT NECESSARY"
echo "If there were no errors in the process so far, it should be fine to proceed with the reboot."
read -r -p "Continue with reboot? [Y/n] " consent
if [[ "$consent" =~ ^([nN])$ ]]
then
    echo "Okay - will not reboot now!"
    exit 1
else
    echo "Proceed with reboot!"
    sudo reboot
fi