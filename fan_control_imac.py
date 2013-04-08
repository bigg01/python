#!/usr/bin/env python
#! -*- coding: utf-8 -*
 
__author__ = "Oliver Guggenbuehl"
__copyright__ = "Copyright 2013, The GUOPY Project"
__credits__ = ["Oliver Guggenbuehl"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Oliver Guggenbuehl"
__email__ = "me@oliver-guggenbuehl.com"
__status__ = "Test"
 
# This program is public domain - Use at your own risk :)
# Copyright 2009 by Matt Ryanczak
#
# I wrote this script for my macbook because I could not find anything else that worked very well.
# The algorithm used to control the fan speed was inspired by a shell script written by Nick Barcet
# His script (for the macbook pro) can be found here: https://wiki.ubuntu.com/MacBookPro/SantaRosaFanControl

"""
 modinfo applesmc
filename:       /lib/modules/3.5.0-21-generic/updates/dkms/applesmc.ko
license:        GPL v2
description:    Apple SMC
author:         Nicolas Boichat
srcversion:     C506F06E9554981B7204912
alias:          dmi*:pn*iMac*:rvn*Apple*:
alias:          dmi*:pn*MacPro*:rvn*Apple*:
alias:          dmi*:pn*Macmini*:rvn*Apple*:
alias:          dmi*:pn*MacBook*:rvn*Apple*:
alias:          dmi*:pn*MacBookPro*:rvn*Apple*:
alias:          dmi*:pn*MacBookAir*:rvn*Apple*:
depends:        input-polldev
vermagic:       3.5.0-21-generic SMP mod_unload modversions
"""


import sys, os
import time
import os
import syslog

DebugLogging = 0

# Tweak these numbers to adjust the sensitivity of the fans
MaxTemp = 62
MinTemp = 47

# These number are tweakable as well but note that 6500 is the highest setting for the fan.
MaxFanSpeed = 3800
# I add 100 to this value before setting the fan speed in the code below. This works better IMHO
MinFanSpeed = 2200



# Daemon spawning function from python cookbook
def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit first parent.
        syslog.syslog(syslog.LOG_NOTICE,'CPU TEMP Monitor startet. Average Temperature: %s speed=1000')
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid( )
    # Perform second fork.
    try:
        pid = os.fork( )
        if pid > 0:
            sys.exit(0) # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush( )
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno( ), sys.stdin.fileno( ))
    os.dup2(so.fileno( ), sys.stdout.fileno( ))
    os.dup2(se.fileno( ), sys.stderr.fileno( ))



# Fork the daemon process
daemonize()




"""
FAN: 1 MIN: 940 MAX: 3800
FAN: 2 MIN: 3124 MAX: 5500
FAN: 3 MIN: 940 MAX: 2100
FAN: 3 MIN: 940 MAX: 2100
"""

syslog.openlog("mb-fancontrol-guo")

# Function to set the fan speed
def SetFanSpeed (FanSpeed, MinFanSpeed):
    try:
        if (FanSpeed < MinFanSpeed):
           FanSpeed = MinFanSpeed
        FanSpeedSysFn = '/sys/devices/platform/applesmc.768/fan1_min'
        FanSpeedSys = open(FanSpeedSysFn, 'w+')
        if (DebugLogging == 1):
            syslog.syslog(syslog.LOG_NOTICE,'Setting fan speed to: %s' % (FanSpeed))
        FanSpeedSys.write(FanSpeed) 
        FanSpeedSys.close()
    except IOError:
        syslog.syslog(syslog.LOG_ERR,'Fatal Error: Cannot open: /sys/devices/platform/applesmc.768/fan1_min. Is the applesmc module loaded?')
    return 1

# Set the initial fan speed to MinFanSpeed
SetFanSpeed(str(MinFanSpeed), str(MinFanSpeed))

def SetMAXFanSpeedCPU (FanSpeed):
 #FanSpeed = FanSpeed
	#for i in range(1,4):
	#speed = int(FanSpeed)
	print FanSpeed
	FanSpeedSysFn = ('/sys/devices/platform/applesmc.768/fan3_min') 
	FanSpeedSys = open(str(FanSpeedSysFn), 'w+')
	FanSpeedSys.write(str(FanSpeed)) 
	print "set %s %s" % (FanSpeedSysFn, FanSpeed)
	FanSpeedSys.close()

def SetMAXFanSpeed ():
	FanSpeed = 1500
	for i in range(1,4):
		FanSpeedSysFn = ('/sys/devices/platform/applesmc.768/fan%s_min' % (int(i)))
		FanSpeedSys = open(str(FanSpeedSysFn), 'w+')
		FanSpeedSys.write(str(FanSpeed)) 
		print "set %s %s" % (FanSpeedSysFn, FanSpeed)
		FanSpeedSys.close()
		# syslog.syslog(syslog.LOG_NOTICE,'Average Temperature: %s' % (float(AverageTemp)/1000))Set the initial fan speed to MinFanSpeed

def ShowFanSpeed (FANnr):
	FAN = ('/sys/devices/platform/applesmc.768/fan%s_min' % (int(FANnr)))
	Temp1Input = open(FAN)
	FANminRPM = int(Temp1Input.read())
	Temp1Input.close()
	FANmax = ('/sys/devices/platform/applesmc.768/fan%s_max' % (int(FANnr)))
	Temp1Input = open(FANmax)
	FANmaxRPM = int(Temp1Input.read())
	Temp1Input.close()
	print 'FAN: %s MIN: %s MAX: %s' % (int(FANnr),int(FANminRPM),int(FANmaxRPM))
	return int(FANminRPM)
"""
[ guo optimus-iMac ~ ]  cat /sys/devices/platform/coretemp.0/temp[0-9]_{label,input,crit_alarm,max}
Core 0
Core 1
Core 2
Core 3
50000
45000
48000
45000
0
0
0
0
83000
83000
83000
83000
"""

def GetCPUTemp (NR):
	#for i in range(2,6):
	FAN = ('/sys/devices/platform/coretemp.0/temp%s_input' % (int(NR)))
	Temp1Input = open(FAN)
	FANminRPM = int(Temp1Input.read())/1000
	Temp1Input.close()
	FANmax = ('/sys/devices/platform/coretemp.0/temp%s_max' % (int(NR)))
	Temp1Input = open(FANmax)
	FANmaxRPM = int(Temp1Input.read())/1000
	Temp1Input.close()
	#print FAN
	print 'CPU temp: %s MIN: %s MAX: %s' % (int(NR),int(FANminRPM),int(FANmaxRPM))
	return int(FANminRPM)
	

ShowFanSpeed(1)
ShowFanSpeed(2)
ShowFanSpeed(3)

#SetMAXFanSpeed()


Temp1InputFn = '/sys/devices/platform/applesmc.768/temp5_input'
Temp2InputFn = '/sys/devices/platform/applesmc.768/temp12_input'
Temp3InputFn = '/sys/devices/platform/applesmc.768/temp4_input'
Temp4InputFn = '/sys/devices/platform/applesmc.768/temp10_input'



#SetFanSpeed(str(FanSpeed), str(MinFanSpeed))
#syslog.syslog(syslog.LOG_NOTICE,' Set Fan CPU guo: %s %s ' % (MinFanSpeed,FanSpeed ))






"""
[ guo optimus-iMac ~ ] cat /sys/devices/platform/applesmc.768/fan2_label 
HDD 
[ guo optimus-iMac ~ ] cat /sys/devices/platform/applesmc.768/fan1_label 
ODD 
[ guo optimus-iMac ~ ] cat /sys/devices/platform/applesmc.768/fan3_label 
CPU 
"""

 
def mastercpufunc():
	FanSpeed=ShowFanSpeed(3)

	CPU2=GetCPUTemp(2)
	CPU3=GetCPUTemp(3)
	CPU4=GetCPUTemp(4)
	CPU5=GetCPUTemp(5)

	AverageTemp = ((CPU2 + CPU3 + CPU4 + CPU5)/4)

	print "average TEMP CPU CORES; %s" % (AverageTemp)

	MAXCPUTEMP = 60

	ALERTCPUTEMP = 74 
	if AverageTemp > MAXCPUTEMP:
		print "alarm cpu"
		if FanSpeed != 1500:
			SetMAXFanSpeedCPU(1500)
			ShowFanSpeed(3)
			syslog.syslog(syslog.LOG_ERR,'CPU ALARM Average Temperature: %s speed=1500' % (float(AverageTemp)))
	else:
		if AverageTemp < MAXCPUTEMP:
			print "ok cpu"
			if FanSpeed != 1000:
				SetMAXFanSpeedCPU(1000)
				ShowFanSpeed(3)
				#syslog.syslog(syslog.LOG_NOTICE,'CPU OK Average Temperature: %s speed=1000' % (AverageTemp))
			
	if AverageTemp > ALERTCPUTEMP:
		print "alarm MAX SPEED needed cpu"
		if FanSpeed != 2100:
			SetMAXFanSpeedCPU(2100)
			ShowFanSpeed(3)
			syslog.syslog(syslog.LOG_ERR,'CPU ALARM MAX SPEED Average Temperature: %s speed=2100' % (float(AverageTemp)))
			print ' Set Fan CPU guo: %s' % (MinFanSpeed)



while True:
    try:
        Temp1Input = open(Temp1InputFn)
        Temp1 = int(Temp1Input.read())
        Temp1Input.close()
        Temp2Input = open(Temp2InputFn)
        Temp2 = int(Temp2Input.read())
        Temp2Input.close() 
        Temp3Input = open(Temp3InputFn)
        Temp3 = int(Temp3Input.read())
        Temp3Input.close()
        Temp4Input = open(Temp4InputFn)
        Temp4 = int(Temp4Input.read())
        Temp4Input.close()
        mastercpufunc()
    except IOError:
        syslog.syslog(syslog.LOG_ERR,'Error opening temperature sensors. Is the applesmc module loaded?')
        continue
    AverageTemp = ((Temp1 + Temp2 + Temp3 + Temp4)/4)
    if (DebugLogging == 1):
        syslog.syslog(syslog.LOG_NOTICE,'Average Temperature: %s' % (float(AverageTemp)/1000))
    if (AverageTemp > (MaxTemp * 1000)):
        SetFanSpeed(str(MaxFanSpeed), str(MinFanSpeed))
        syslog.syslog(syslog.LOG_NOTICE,'Getting too hot! Setting fan speed to: %s' % (MaxFanSpeed))
    else:
        FanSpeed = (((AverageTemp - (MinTemp * 1000)) * (6000 / (MaxTemp - MinTemp)) / 1000))
        SetFanSpeed(str(FanSpeed), str(MinFanSpeed))
    time.sleep(5)    
