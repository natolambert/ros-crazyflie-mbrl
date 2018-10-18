#!/usr/bin/env python2.7

# torch
import torch
from torch.nn import MSELoss

# controller object
from controllers import  MPController

# misc packages
import numpy as np
import time
import matplotlib.pyplot as plt

# our utils
from utils import *

############# ROS INTEGRATION ################

import rospy
import rospkg
import os

# our messages
from crazyflie_driver.msg import MotorControl, MotorControlwID, GenericLogData, LogBlock, Hover

# print settings
np.set_printoptions(precision=3, suppress=True, linewidth=np.nan, threshold=np.nan)
rp = rospkg.RosPack()

#############  UTILS THAT USE GLOBAL VARIABLES ##############################

# returns the elapsed milliseconds since the start of the program
def millis():
    global start_time
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def clear_terminal():
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')

############# Packet Callback ##############################
# Logs the new data and sends a control packet with the current control
# operates at aroud 350Hz

def callback(data):
    # Starts by blocking read/write errors (won't read while fetching)
    fetching_data = True

    # frequency tracker
    global totalReceived
    totalReceived += 1

    # ROS Timestamp. Should analyze this more
    t = data.header.stamp       # note - this may be ROS time

    # pwms
    p = np.zeros([1])
    p[0] = data.values[-2]

    # battery
    b = np.zeros([1])
    b[0] = data.values[-1]

    # Linear accle
    l = np.zeros([1])
    l[0] = data.values[1]

    # angular accel
    a = np.zeros([1])
    a[0] = data.values[0]

    # process packed data
    pwms = unpack_cf_pwm(p)
    imu = unpack_cf_imu(l,a)

    # if packaging Eulers
    if False:
        # ypr
        ypr_p = np.zeros([1])
        ypr_p[0] = data.values[2]
        ypr = unpack_cf_ypr(ypr_p)

    # Else Eulers are floats
    else:
        ypr = np.zeros([1,3])
        ypr[0][1] = data.values[2]  #Pitch
        ypr[0][2] = data.values[3]  #Roll
        ypr[0][0] = data.values[4]  #Yaw

    # Assignment of individual variables to the global state
    x_prev[0] = imu[0][0]
    x_prev[1] = imu[0][1]
    x_prev[2] = imu[0][2]
    x_prev[3] = ypr[0][1] #pitch
    x_prev[4] = ypr[0][2] #roll
    x_prev[5] = ypr[0][0] #yaw
    x_prev[6] = imu[0][3] #l_x
    x_prev[7] = imu[0][4] #l_y
    x_prev[8] = imu[0][5] #l_z
    x_prev[9] = b[0]      # battery

    ts[0] = str(t)
    pwms_received[0] = pwms[0][0]
    pwms_received[1] = pwms[0][1]
    pwms_received[2] = pwms[0][2]
    pwms_received[3] = pwms[0][3]

    # No longer log packet ID because not enough space in log block
    # packet_id_temp = np.zeros([1])
    # packet_id_temp[0] = data.values[-1]
    # packet_id_rec[0] = int(packet_id_temp[0])

    # print('packet')

    # wrap around issues
    x_prev[x_prev == -90] = 0

    # Checks for collision or dangerous state
    if ((abs(x_prev[3]) >= uncontrollable_state) or
        (abs(x_prev[4]) >= uncontrollable_state) or
        (abs(x_prev[6])+abs(x_prev[7])  >= 10) or
        # ( <= -6) or
        (x_prev[8] <= -6) or
        (abs(x_prev_delta[0]) > 70) or
        (abs(x_prev_delta[1]) > 70) or
        (abs(x_prev_delta[2]) > 70) ):
        global stop
        stop = True


    # Send the current message too
    publisher(pub, msg)
    if logging: logger(log)

    # Not assigning data anymore
    fetching_data = False

# This object is called to actually control the crazyflie!
def nodecontroller():

    # We now always log. Start at false to not fill up with 0s
    global logging
    logging = False

    # important varaible for how many previous states to feed to the network
    numStack = 4
    #set to 3 for 50Hz (as per Roberto)

    # equilibrium values from PID control
    # PWMequil = np.array([36334., 36847.,	39682.,	33483.])
    PWMequil = np.array([31687.1,	37954.7,	33384.8,	36220.11]) # new quad

    # store objective here later
    OBJ = np.array([0])

    ############################## callback variables ##########################

    # global because used in radio callback
    global uncontrollable_state
    uncontrollable_state =  27.5
    global stop
    stop = False

    global x_prev
    x_prev = np.zeros(10)
    global pwms_received
    pwms_received = np.zeros(4)
    global ts
    ts = np.zeros(1)

    # controller & logging variables
    global x_prev_cached
    x_prev_cached = np.zeros(10)

    global x_prev_delta
    x_prev_delta = np.zeros(10)

    global ts_cached
    ts_cached = np.zeros(1)
    pwms_cached = np.zeros(4)

    pwms_avg = PWMequil
    controlTicks = np.zeros(1)
    packet_id_rec = np.zeros(1)   # added

    u = np.zeros([4])

    ############################## timing variables ############################

    # global start_time for freq calculations
    start_time = datetime.now()
    start_time = millis()

    global totalReceived
    totalReceived = 0

    ############################## flags & runtime adjustments #################

    # declare packet_id coutner
    packet_id = 0

    # Take off and radio spinup flags
    take_off_flag = False

    #global spinup = True

    global caughtFlag
    global caughtRuns
    global caughtTime
    global Spinup
    Spinup = True
    caughtTime = 0
    caughtFlag = False
    caughtRuns = 0

    # for sleep call. sent if we update the control that is being sent fast
    global sent
    sent = False

    # POWER ADJUSTMENTS
    takeoff_power = 1.22
    equilAdjust = takeoff_power-1
    takeoff_adjust = 0.3
    takeoff_adjust_step = .013 #007
    equil_step = .95
    hop_power = 0
    takeoff_time = 900
    hop_time = 0
    spin_time = 250
    hop_delay = 500

    fetching_data = False
    Spinup = True

    ############################## Logging and ROS ##########################
    global log
    timestr = time.strftime("%Y%m%d-%H%M%S")
    log_folder = "/home/hiro/crazyflie_ros/src/crazyflie_mpc/src/_flightlogs/_newquad1/packet_test/"
    log = open(log_folder+'flight_log-'+timestr+'.csv',"w+")

    global pub
    pub = rospy.Publisher('/cmd_vel', MotorControlwID, queue_size = 1)
    pubCont = rospy.Publisher('/cmd_hover', Hover, queue_size = 1)

    rospy.init_node('MPController', anonymous=True)
    rospy.Subscriber('/state_data', GenericLogData, callback)

    rate = rospy.Rate(150) # frequency of operation in hz

    # just update the message values to send a new control
    global msg
    msg = MotorControlwID()


    ################################ MPC ####################################
    #mpc1 = MPController(newNN, crazy, dt_x, dt_u, origin_minimizer, N=100, T=5, variance = 1000)
    mpc1 = MPController(PWMequil, N=4000, T=2, variance =6000, numStack = numStack)
    print('...MPC Running')

    stopFlag = False
    plot_each = True
    takecount = 0

    # stacked states to pass into network
    pred_state = torch.zeros(9)
    x_prev_stacked = np.zeros(numStack*9)
    u_prev_stacked = np.ones(numStack*4)*30000. # initial U stacked is defined here

    # start logging right as we start
    logging = True

    while not rospy.is_shutdown():

        # update state variables used for control
        if not fetching_data:
            x_prev_delta = x_prev - x_prev_cached
            x_prev_cached = x_prev #change from LAST state
            ts_cached = int(ts)
            if Spinup:
                new_data = True
            else:
                new_data = not np.array_equal(x_prev_cached[:9], x_prev_stacked[:9])
                # new_data = not np.array_equal(x_prev_cached[3:6], x_prev_stacked[3:6])


        ############################ EMERGENCY STOP  ###########################

        if stop:
            logging = False
            msg.m1 = 0
            msg.m2 = 0
            msg.m3 = 0
            msg.m4 = 0
            msg.ID = 9999
            publisher(pub, msg)

            print "EMERGENCY SHUTDOWN. Entered uncontrollable state: ", x_prev_cached[3], x_prev_cached[4], x_prev_cached[5]
            print x_prev_delta[0], x_prev_delta[1], x_prev_delta[2], x_prev_cached[6], x_prev_cached[7], x_prev_cached[8]

            sent = True

            if stopFlag:
                log.close()
                print "Final::: On Control Freq Hz = ", (caughtRuns /((millis()-caughtTime)/1000))
                print "Fianl::: Packet Rx Freq Hz = ", (totalReceived/((millis())/1000))

                ############################ PLOT EACH RUN ####################################
                if plot_each:
                    with open(log_folder+'flight_log-'+timestr+'.csv') as csvfile:
                        # Load pwm and euler values
                        logged_dat = np.loadtxt(csvfile, delimiter =",")

                        Euler = logged_dat[:,3:5]
                        PWM = logged_dat[:,9:13]

                        # Plot pwm values
                        ax1 = plt.subplot(211)
                        ax1.plot(PWM[:,0], label='M1')
                        ax1.plot(PWM[:,1], label='M2')
                        ax1.plot(PWM[:,2], label='M3')
                        ax1.plot(PWM[:,3], label='M4')
                        ax1.legend(loc=2)
                        ax1.set_title('FLIGHT PWMS / EULER')
                        ax1.set_xlabel('PACKET NUMBER')
                        ax1.set_ylabel("PWM VALUES")

                        # plot euler angles
                        ax2 = plt.subplot(212)
                        ax2.plot(Euler[:,0], label='PITCH')
                        ax2.plot(Euler[:,1], label='ROLL')
                        ax2.legend(loc=2)
                        ax2.set_xlabel('PACKET NUMBER')
                        ax2.set_ylabel("EULER ANGLES (DEG)")

                        plt.savefig("flightplots/"+timestr)
                        plt.show()

                quit()
            stopFlag= True


        ########################### Takeoff ############################
        if ((millis()-start_time) >= hop_delay + spin_time) and not take_off_flag and not Spinup:
            mean = PWMequil

            # only bother computing when there's new data
            if new_data:
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = x_prev_cached[:9]

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = pwms_received

                takeoff_adjust += takeoff_adjust_step
                pow = min(takeoff_power,takeoff_adjust)
                # print(pow)
                u, objval, pred_state = mpc1.update(x_prev_stacked,u_prev_stacked,pow)   # UPDATE SHOULD RETURN PWMs
                u = u[:4]

                msg.m1 = min(max(u[0], 0), 65535)
                msg.m2 = min(max(u[1], 0), 65535)
                msg.m3 = min(max(u[2], 0), 65535)
                msg.m4 = min(max(u[3], 0), 65535)
                msg.ID = packet_id

                packet_id += 1
                takecount += 1

                print('OPEN LOOP TAKEOFF (RUN)')
                if (millis()-start_time) >= (takeoff_time + spin_time + hop_delay):
                    take_off_flag = True

                publisher(pub, msg)
                # if logging: logger(log)
                sent = True





        ############################ CONTROLLED FLIGHT     ############################

        elif ((millis()-start_time) >= (takeoff_time + spin_time + hop_delay)):

            # only bother computing when there's new data
            if new_data:
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = x_prev_cached[:9]

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = pwms_received

                equilAdjust = equil_step*equilAdjust
                u, objval, pred_state = mpc1.update(x_prev_stacked,u_prev_stacked,1.05)   # UPDATE SHOULD RETURN PWMs
                u = u[:4]
                OBJ[0] = objval.cpu().detach().numpy()

                # prep packet
                if caughtTime == 0:
                    caughtTime = millis()
                    caughtFlag = True

                msg.m1 = min(max(u[0], 0), 65535)
                msg.m2 = min(max(u[1], 0), 65535)
                msg.m3 = min(max(u[2], 0), 65535)
                msg.m4 = min(max(u[3], 0), 65535)
                msg.ID = packet_id
                publisher(pub, msg)

                packet_id += 1 # update packet ID on each update of control
                caughtRuns += 1
                # if logging: logger(log)

                sent = True

        ##################### RADIO SPINUP #######################################
        # spams 0s when getting the radio up to speed
        if (millis()-start_time) < spin_time:
            msg.m1 = 0
            msg.m2 = 0
            msg.m3 = 0
            msg.m4 = 0
            msg.ID = 0
            pub.publish(msg)
            sent = True
        else:
            Spinup = False

        if sent:
            sent = False
            rate.sleep()


def logger(log):
     log.write("{0},{1},{2},{3},{4},{5},".format(str(x_prev_cached[0]),str(x_prev_cached[1]),str(x_prev_cached[2]),str(x_prev_cached[3]),str(x_prev_cached[4]),str(x_prev_cached[5])))
     # Log raw lienar accel`
     log.write("{0},{1},{2},".format(str(x_prev_cached[6]),str(x_prev_cached[7]),str(x_prev_cached[8])))
     # log past PWM values
     log.write("{0},{1},{2},{3},".format(pwms_received[0],pwms_received[1],pwms_received[2],pwms_received[3]))
     # Log time stamp
     log.write("{0},{1},".format(str(ts_cached),'-1'))#str(objval.cpu().detach().numpy())))
     log.write("{0}".format(str(x_prev_cached[-1])))
     # print("battery is...", x_prev_cached[-1])
     log.write('\n')

def publisher(pub, msg):
    pub.publish(msg)
    # print "Objective: ", OBJ
    # print msg.m1, msg.m2, msg.m3, msg.m4
    # print "Message :", msg.ID
    # print "CF PWM :" , pwms_received, "\n"
    # print "Packet ID: ", packet_id_rec, "\n"
    # print "Total Radio Loop Freq Hz = ", (totalRuns / (millis() / 1000)) #Frequency control is SENT
    if caughtFlag and totalReceived % 350 == 0:
        print "On Control Freq Hz = ", (caughtRuns /((millis()-caughtTime)/1000))
        print "Packet Rx Freq Hz = ", (totalReceived/((millis())/1000))

if __name__ == '__main__':
    nodecontroller()
