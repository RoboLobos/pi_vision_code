#!/bin/bash  -x
. ~/.bashrc
cd /home/pi
cur=`basename loggy/*`
next=$((cur+1))
mv loggy/$cur loggy/$next
if [ -f ./team2359/output.avi ]; then
  echo "found it!"
  mv output.avi ${cur}_output.avi
else
  echo "not here!"
fi
#cd /home/pi/2359
#mv jpg ${cur}_jpg
#mkdir jpg
#
# 65 too bright for recorded video
#
#/usr/bin/v4l2-ctl --set-ctrl brightness=65 -d /dev/video0
#/usr/bin/v4l2-ctl --set-ctrl brightness=50 -d /dev/video0
#/usr/bin/v4l2-ctl --set-ctrl brightness=25 -d /dev/video0
#/usr/bin/v4l2-ctl --set-ctrl brightness=30 -d /dev/video0
#/usr/bin/v4l2-ctl --set-ctrl brightness=35 -d /dev/video0
#/usr/bin/v4l2-ctl --set-ctrl brightness=40 -d /dev/video0
#nohup  /home/pi/video.py > video_error 2>&1 &
cd /home/pi/2359
mv jpg ${cur}_jpg
mkdir -p jpg/5802 jpg/5803

sleep 8

export SONAR_PROC_EXISTS=`ps -ef|grep python|grep sonar|grep -v grep|wc -l`
echo $SONAR_PROC_EXISTS
if [ $SONAR_PROC_EXISTS -gt 1 ]; then
  echo "processes exist"
  kill -9 `ps -ef|grep sonar|grep -v grep | awk '{print $2}'`
fi 

export CAM_PROC_EXISTS=`ps -ef|grep python|grep pi_cam_stream|grep -v grep|wc -l`
echo $CAM_PROC_EXISTS
if [ $CAM_PROC_EXISTS -gt 1 ]; then
  echo "processes exist"
  kill -9 `ps -ef|grep pi_cam|grep -v grep | awk '{print $2}'`
fi 

export PI_IP_ADDR=`ip a|grep -w eth0 -A 3|grep -iw inet|awk '{print $2}'|awk -F\/ '{print $1}'`
#export PI_IP_ADDR=`ip a|grep eth0|grep -w inet|awk '{print $2}'|awk -F\/ '{print $1}'`

echo $PI_IP_ADDR > ip_addr_here.txt

nohup /home/pi/2359/pi_cam_stream_5802.py $PI_IP_ADDR 5802 &
#nohup /home/pi/2359/pi_cam_stream_5803.py $PI_IP_ADDR 5803 &
#nohup /home/pi/2359/sonar.py&
#nohup /home/pi/2359/pi_left.py&
