#!/usr/bin/python3
'''
	Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server - modified to work with Python 3 - mrc

	Contour processing - brookshank - github

	Additional stuff - mrc - Team 2359
'''
import sys
import cv2
#import Image
#import PIL as pillow
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
#from SocketServer import ThreadingMixIn
from io import BytesIO
from io import StringIO
import io
import time
import socket
import math
import RPi.GPIO as GPIO
from networktables import NetworkTables

#from GripPipelineTue import GripPipeline
from minime import GripPipeline
#from owengrip import GripPipeline

#image_scale = 0.5
image_scale = 1.0
#x_resolution = 640
#y_resolution = 480
#x_resolution = 320
#y_resolution = 240
#x_resolution = 160
#y_resolution = 120
x_resolution = 60
y_resolution = 40
good = 0


def extra_processing(pipeline):
    extra_processing_start = time.time()
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    print("in extra_processing")
    global NTtable 
    distance = 0.0
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []
    areas = []
    kount = 0
    x0 = 0
    x1 = 0
    kontour_kountr = 0
    print("*******kontour_kountr: ",kontour_kountr)
    if kontour_kountr > 0:
        return 1
    for contour in pipeline.filter_contours_output:
        print("this is in the for loop: ",kontour_kountr)
        if kontour_kountr>0:
            print("not a good sample - one contour!")
            return 1
        elif kontour_kountr>2:
            print("not a good sample - more than two!")
            return 1
        #if kontour_kountr>1:
            #print("not a good sample - one contour")
            #print("Total contours: ",kontour_kountr)
            #return 1
        #
        # commented mrc - 20180216
        #
        kontour_kountr += 1
    for contour in pipeline.filter_contours_output:
        print("kount",kount)
        #print("in contours")
        #if kount%2 == 0:
        x, y, w, h = cv2.boundingRect(contour)
        print("x,y,w,h",x,y,w,h)
        if kount == 0:
            x0 = int(x*image_scale)
            x1 = int((x+w)*image_scale)
        if kount == 1:
            x1 = int((x+w)*image_scale)
        #print(x_resolution/2)
        #if x > x_resolution*image_scale*0.5:
            #print("go left")
        #elif x < x_resolution*image_scale*0.5:
            #print("go right")
        center_x_positions.append(x*image_scale + w * image_scale)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y*image_scale + h * image_scale)
        widths.append(w*image_scale)
        heights.append(h*image_scale)
        areas.append(w*image_scale * h*image_scale)
        '''
        here we use trigonometry to determine the distance from the object, given that
        the object is t cm wide and the camera captures d degrees
        '''
        #t = 70 # use for switch
        t = 130 # use for switch
        #t = 30 # use for switch
        d = 70
        #d = 30
        height, width, channels = contour.shape
        #print('width: ', width)
        #print('Target width: ' , w)
        v = (t/(w/width)) #*image_scale# w is how many pixels wide is the object
        #print ('pixel width:',v)
        tilt = -1 #the tilt of the camera, in degrees
        kount += 1
    # uncomment next line if you want calculation based on image - 20180210 mrc
    #sae_val = (distance*39.37007874*image_scale)-2
    #NTtable = NetworkTables.getTable('switch')
    #NTtable = NetworkTables.getTable('switch')
    #GPIO.setmode(GPIO.BCM)
    #TRIG=23
    #ECHO=24
    #GPIO.setup(TRIG,GPIO.OUT)
    #GPIO.setup(ECHO,GPIO.IN)
    #GPIO.output(TRIG,False)
    #time.sleep(0.00001)
    #time.sleep(2)

    #GPIO.output(TRIG,True)
    #time.sleep(0.00001)
    #GPIO.output(TRIG,False)
    #pulse_start=time.time()
    #pulse_end=time.time()
    
    #while GPIO.input(ECHO)==0:
        #pulse_start=time.time()
   # 
    #while GPIO.input(ECHO)==1:
        #pulse_end=time.time()
   # 
    #pulse_duration=pulse_end-pulse_start
    #sonar_dist=pulse_duration*17150
    #sonar_dist=round(sonar_dist/2.54,1)-.5
    #print("sonar dist:",sonar_dist," inches")
    #GPIO.cleanup()
    #distance = sonar_dist
    #nt_put_time_start = time.time()
    #NTtable.putValue('dist',sonar_dist)
    #nt_put_time_end = time.time()
    #print("nt time: ",nt_put_time_end - nt_put_time_start)
    #if sae_val > 18:
        #print( 'SAE from cam: ',sae_val) #(distance*39.37007874*image_scale)-2)
        #NTtable.putValue('dist',sae_val)
    #else:
        #print( 'From sonar: ',sonar_dist)



def draw_contours(pipeline, frame):  # TODO combine this with extra_processing
    draw_contours_start = time.time()
    """
    Draws and labels contours on actual image, useful to see what opencv "sees".
    :param pipeline: the pipeline that just processed an image
    :param frame: the image directly from the camera
    :return: edited frame, sent to disk to be used in mjpg stream
    """
    x0 = 0
    x1 = 0
    contour_number = 0
    contour_frame_start = time.time()
    contour_frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale,interpolation = cv2.INTER_CUBIC)
    contour_frame_end = time.time()
    print("contour_frame_start_end: ",contour_frame_end-contour_frame_start)
    #contour_frame = cv2.resize(frame, (0, 0), fx=image_scale, fy=image_scale)
    kontour_kountr = 0
    filter_contours_start = time.time()
    for contour in pipeline.filter_contours_output:
        print("in the  for contour in pipeline.filter_contours_output")
        if kontour_kountr>0:
            #print("not a good sample - one contour!")
            return 1
        elif kontour_kountr>2:
            print("not a good sample - more than two!")
            return 1
        kontour_kountr += 1
    #if kontour_kountr == 2:
        #print("2 contours!")
    filter_contours_end = time.time()
    print("filter_contours_start_end: ",filter_contours_end - filter_contours_start)
    for contour in pipeline.filter_contours_output:
        print("contour_number in pipeline.filter_contours_output:",contour_number)
        x, y, w, h = cv2.boundingRect(contour)
        if contour_number == 0:
            x0 = x
        if contour_number == 1:
            x1 = x+w
        #if x > x_resolution*image_scale*.5:
            #print("right side")
        #if x < x_resolution*image_scale*.5:
            #print("left side")
        print("Draw contours* x,y,w,h:",x,y,w,h)
        #print("x+w:",x+w)
        center = (x*image_scale + (w * image_scale)), (y*image_scale + (h * image_scale))
        #
        # this is incorrect - need to figure out the correct center
        #
        #if contour_number%2 == 0:
        #print("Center:",center)
        contour_target_circle_start = time.time()
        cv2.circle(contour_frame,(int(x*image_scale),int(y*image_scale)),5,(0,255,0),-1)
        cv2.circle(contour_frame,(int((x+w)*image_scale),int(y*image_scale)),5,(0,255,0),-1)
        (cv2.drawContours(contour_frame, pipeline.filter_contours_output, -1, (255, 0, 120), 3))
        contour_target_circle_end = time.time()
        print("contour_target_circle: ",contour_target_circle_end - contour_target_circle_start)
        #(cv2.drawContours(contour_frame, pipeline.filter_contours_output, -1, (255, 0, 120), cv2.FILLED))
        contour_rectangle_start = time.time()
        height, width, channels = contour_frame.shape
        cv2.rectangle(frame, (x, y), (x+w,y+h), (255, 255, 0), 1)
        contour_rectangle_end = time.time()
        print("contour_rectanle_stuff: ",contour_rectangle_end-contour_rectangle_start)
        #
        # 20180216 mrc - commented next two lines to see if we can speed things up
        #
        #cv2.line(contour_frame, (int(width*.5),0), (int(width*.5), int(height)), (50,205,50),2)
        #cv2.line(contour_frame, (0,int(height*.5)), (int(width), int(height*.5)), (50,205,50),2)
        contour_number += 1

    #print("x0:",x0-x_resolution*.5*image_scale*.8,"x1:",x_resolution*.5*image_scale-x1*.8)
    #print("x0:",x0-x_resolution*.5*image_scale,"x1:",x_resolution*.5*image_scale-x1)
    #if ((x0-x_resolution*.5*image_scale*.8) >= (x_resolution*.5*image_scale-x1 )) and ((x_resolution*.5*image_scale-x1*.8) >= (x0-x_resolution*.5*image_scale )):
        #print("x0:",x0-x_resolution*.5*image_scale*.8,"x1:",x_resolution*.5*image_scale-x1*.8)
        #print("go forward")
    #elif ((x0-x_resolution*.5*image_scale) < (x_resolution*.5*image_scale-x1 )):
    ##if (x0-x_resolution*.5*image_scale*.8) > (x0-x_resolution*.5*image_scale):
        #print("x0:",x0-x_resolution*.5*image_scale,"x1:",x_resolution*.5*image_scale-x1)
        #print("go left")
    #elif ((x0-x_resolution*.5*image_scale) > (x_resolution*.5*image_scale-x1)):
    ##if (x_resolution*.5*image_scale-x1*.8) > (x_resolution*.5*image_scale-x1):
        #print("x0:",x0-x_resolution*.5*image_scale,"x1:",x_resolution*.5*image_scale-x1)
        #print("go right")
    draw_contours_end = time.time()
    print("draw contours time: ",draw_contours_end - draw_contours_start)
    return contour_frame



capture=None




class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			#self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--boundary')
			self.end_headers()
			current_frame=0
			while True:
				try:
					start_time = time.time()
					rc,frame = capture.read()
					frame_capture_end = time.time()
					#print("frame capture time: ",frame_capture_end - start_time)
					if not rc:
					    continue
					#
					# uncomment the next line to save the stream seen by the driver
					#
					#cv2.imwrite("./jpg/5802/%s.jpg"  % str(current_frame).zfill(8),frame)
					#img_string_nm="./jpg/"+pi_port+"/frame_%d.jpg"
					#cv2.imwrite(img_string_nm  %str(current_frame).zfill(8),frame)
					#cv2.imwrite("./jpg/"+str(pi_port)+"/frame_%s.jpg"  %str(current_frame).zfill(8),frame)
					#before_pipeline_process = time.time()
					#good = pipeline.process(frame)
					#after_pipeline_process = time.time()
					#print("after good stuff: ",after_pipeline_process-before_pipeline_process)
					#after_pipeline_process = time.time()
					#print("pipeline_process time: ",after_pipeline_process - start_time)
					good=0
					#print("return from pipeline: ",good)
					if good != 1:
                                            #extra_processing(pipeline)
                                            good = 0
                                            #print("frame:",current_frame)
                                            #
                                            #
                                            # commented 20180216 mrc - testing speed of stream
                                            #
                                            #
                                            #cv2.imwrite("./jpg/switch/draw_contour_%s.jpg" % str(current_frame).zfill(8), draw_contours(pipeline, frame))
                                            #draw_contours(pipeline, frame)
                                            #frame_to_write = draw_contours(pipeline, frame)
                                            #cv2.imwrite("./jpg/switch/%s.jpg"  % str(current_frame).zfill(8),frame)
                                            #uncomment next line to write based on contours
                                            #cv2.imwrite("./jpg/switch/contour_%s.jpg" % str(current_frame).zfill(8),frame_to_write)
                                            #cv2.imwrite("./jpg/switch%d.jpg"  %current_frame,draw_contours(pipeline, frame))
                                            current_frame += 1
                                            #imgRGB=cv2.cvtColor(frame_to_write,cv2.COLOR_BGR2RGB)
                                            #
                                            # uncomment next line to stream unchanged frame
                                            imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                                            # uncomment next line to use image without targeting
                                            #imgRGB=cv2.cvtColor(framey,cv2.COLOR_BGR2RGB)
                                            r, buf = cv2.imencode(".jpg",imgRGB)
                                            jpg = Image.fromarray(imgRGB)
                                            self.wfile.write(b"--boundary\r\n")
                                            self.send_header('Content-type','image/jpeg')
                                            self.send_header('Content-length',str(len(buf)))
                                            self.end_headers()
                                            self.wfile.write(bytearray(buf))
                                            #jpg.save(self.wfile,'JPEG')
                                            self.wfile.write(b'\r\n')
                                            time.sleep(0.001)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.mjpg'):
			if current_frame == 0:
                           #with urllib.request.urlopen("ras1.local:5802/cam.mjpg") as response:
                           #with urllib.request.urlopen("10.23.59.12:5802/cam.mjpg") as response:
                           with urllib.request.urlopen(pi_cam_urltoopen) as response:
                               html = response.read()
		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			#self.wfile.write('<img src="http://ras1.local:5802/cam.mjpg"/>')
			#self.wfile.write('<img src="http://10.23.59.12:5802/cam.mjpg"/>')
			#self.wfile.write('<img src="http://169.254.16.100:5802/cam.mjpg"/>')
			#self.wfile.write('<img src="http://10.23.59.60:9091/cam.mjpg"/>')
			#self.wfile.write('<img src="http://10.23.59.128:9091/cam.mjpg"/>')
			self.wfile.write(pi_cam_url)
			self.wfile.write('</body></html>')
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	global pi_addr
	global pi_port
	pi_addr=sys.argv[1]
	pi_port=sys.argv[2]
	print("pi_addr: ",pi_addr)
	print("pi_port: ",pi_port)
	global capture
	global current_frame
	global pi_cam_url
	pi_cam_url="'<img src=\"http://"+pi_addr+":"+pi_port+"/cam.mjpg\"/>'"
	print("pi_cam_url: ",pi_cam_url)
	global pi_cam_urltoopen
	pi_cam_urltoopen=pi_addr+":"+pi_port+"/cam.mjpg"
	print("pi_cam_urltoopen: ",pi_cam_urltoopen)
	host_ip_addr=socket.gethostbyname('ras1.local')
	print("host_ip_addr: %s",host_ip_addr)
	global pipeline 
	global x0,x1 
	pipeline = GripPipeline()
	capture = cv2.VideoCapture(0)
	capture.set(3, x_resolution); 
	capture.set(4, y_resolution);
	capture.set(5,30);
	global frame

	NetworkTables.initialize(server=host_ip_addr)
	NetworkTables.setServerTeam(2359,port=1735)
	#NetworkTables.setServerTeam(2359,port=5082)
	#NetworkTables.initialize(server='roboRIO-2359-FRC.local')
	#NetworkTables.initialize(server='169.254.156.122')
	#NetworkTables.setClientMode()
	print("after init")
	#NetworkTables.initialize(server='192.168.1.26')
	#NetworkTables.initialize(server='127.0.0.1')
	try:
		#server = ThreadedHTTPServer(('ras1.local', 5802), CamHandler)
		#server = ThreadedHTTPServer(('10.23.59.12', 5802), CamHandler)
		#server = ThreadedHTTPServer(('169.254.16.100', 5802), CamHandler)
		#server = ThreadedHTTPServer(('10.23.59.60', 9091), CamHandler)
		#server = ThreadedHTTPServer(('10.23.59.128', 9091), CamHandler)
		server = ThreadedHTTPServer((pi_addr, int(pi_port)), CamHandler)
		print("server started")
		#if current_frame == 0:
                    #with urllib.request.urlopen("10.23.59.60:5002/cam.mjpg") as resopnse:
                        #html = response.read()
		server.serve_forever()

	except KeyboardInterrupt:
		capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()

