#!/bin/bash

#
export START_STOP_STATUS=$1
export PATH=$PATH:/usr/local/bin:/usr/local/sysbin
echo $START_STOP_STATUS
cd /home/pi
start_stop_status()
{
if [ "$START_STOP_STATUS" = "start" ]; then
    cd /home/pi
    touch trying_to_start
    #su - pi -c ". ~/.profile;cd /home/pi;nohup ./video.py &"
    su - pi -c ". ~/.bashrc;nohup /home/pi/launcher.sh&"
    echo "working">./working_here.txt
    if [ $? -ne 0 ]; then
       echo "working">./not_working_here.txt
       echo "An error may have occurred while starting ALL applications"
       exit 1
    fi
    #touch /var/lock/subsys/applications
fi

if [ $START_STOP_STATUS = "stop" ]; then
    cd /home/pi
    echo "stop section">./stop_working_here.txt
    kill -9 `ps -ef|grep pi_cam_stream|grep -v grep | awk '{print $2}'`
    if [ $? -ne 0 ]; then
       echo "An error may have occurred while stopping ALL applications"
       exit 1
    fi
fi

if [ "$START_STOP_STAUTS" = "status" ]; then
    ps -ef|grep pi_ubuntu|grep -v grep
fi
}
echo "*****"
echo "*****"
echo "*****"
echo "*****"
echo "*****"
echo "Team 2359 daemon action:  $START_STOP_TEST"
echo "*****"
echo "*****"
echo "*****"
echo "*****"
echo "*****"
if [ $START_STOP_STATUS = "start" ]; then
    start_stop_status
elif [ $START_STOP_STATUS = "stop" ]; then
    start_stop_status
elif [ $START_STOP_STATUS = "test" ]; then
    start_stop_status
fi
