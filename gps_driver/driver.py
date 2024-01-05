#!/usr/bin/env python3

import serial
import rospy
import utm
from gps_driver.msg import gps_msg
from std_msgs.msg import String
import sys
SENSOR_NAME = 'GPS'

if __name__ == '__main__':
    #if len(sys.argv)>0:
        #rospy.loginfo(sys.argv[1])
    SENSOR_NAME = 'GPS'
    rospy.init_node("gps")
    serial_port = rospy.get_param('~port','/dev/ttyUSB0')
    serial_baud = rospy.get_param('~baudrate',4800)
    sampling_rate = rospy.get_param('~sampling_rate',20.0)

    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    gps=gps_msg()
    gps_pub=rospy.Publisher(SENSOR_NAME,gps_msg,queue_size=5)
    
    
    
    gps.header.frame_id='GPS1_Frame'
   
    sleep_time = 1/sampling_rate - 0.025
    
    try:
        while not rospy.is_shutdown():
            
   
            line = port.readline()
            line=str(line)
            line1=line.split(",")
            #rospy.loginfo(line)
            #rospy.loginfo(line1)
            #print line
            if line1[2] == '':
                rospy.logwarn("No data")

            else:
                if line.startswith("b'$GPGGA"):
                    
                    coordinate = utm.from_latlon(float(line1[2])/100, float(line1[4])/100)
                    timestamp=str(float(line1[1]))
                    second=(int(timestamp[0:2])*3600)+(int(timestamp[2:4])*60)+int(timestamp[4:6])
                    nsecond=int(float(line1[1][6:]))
                    #rospy.loginfo(float(line1[4])/1000)
                    #stampid=float(line1[1])
                    latd=int(float(line1[2]))//100
                    latm=float(line1[2])-(100*latd)
                    lat= latd+(latm/60)
                    lat=float(lat)

                    lond=int(float(line1[4]))/100
                    lonm=float(line1[4])-(100*lond)
                    lon= lond+(lonm/60)
                    if(line1[5]=='W'):
                        lon*=-1
                    lon=float(lon)

                    alt=float(line1[9])/100
                    
                    utme=float(coordinate[0]/100)
                    
                    utmn=float(coordinate[1]/100)
                    
                    zone=float(coordinate[2])
                    
                    letter=coordinate[3]
                    
                    #gps_msg.header.stamp=timestamp
                    gps.header.stamp.secs=second
                    gps.header.stamp.nsecs=nsecond
                    gps.Latitude=lat
                    gps.Longitude=lon
                    gps.Altitude=alt
                    gps.UTM_easting=utme
                    gps.UTM_northing=utmn
                    gps.Zone=zone
                    gps.Letter=letter
                    gps_list=[timestamp,second,nsecond,lat,lon,alt,utme,utmn,zone,letter]

                    rospy.loginfo(gps_list)

                    gps_pub.publish(gps)
                    #gps_pub.publish(letter)
                    
            rospy.sleep(sleep_time)
            
    except rospy.ROSInterruptException:
        port.close()
    
    except serial.serialutil.SerialException:
        rospy.loginfo("Shutting down paro_depth node...")