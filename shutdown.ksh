#!/bin/bash

echo "*****************************"
echo "***** SHUTTING DOWN NOW *****"
echo "*****************************"
#sudo su -
#init 0
kill -9 `ps -ef|grep pi_cam_stream|grep -v grep | awk '{print $2}'`
kill -9 `ps -ef|grep pi_switch|grep -v grep | awk '{print $2}'`
kill -9 `ps -ef|grep -w sonar.py|grep -v grep | awk '{print $2}'`
#sudo systemctl stop motion
sudo shutdown -h now
exit
