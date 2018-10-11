#!/usr/bin/env python2.7


import torch
from torch.nn import MSELoss

from controllers import  MPController
# from dynamics_ionocraft import IonoCraft
# from dynamics_crazyflie_linearized import CrazyFlie
# from dynamics import *
import numpy as np
import time
import matplotlib.pyplot as plt
from utils_data import *

np.set_printoptions(precision=3, suppress=True, linewidth=np.nan, threshold=np.nan)





logging = False


numStack = 4
#set to 3 for 50Hz (as per Roberto)


PWMequil = np.array([36334., 36847.,	39682.,	33483.])
PWMequil = np.array([31687.1,	37954.7,	33384.8,	36220.11]) # new quad

PWMdelta = np.array([0,0,0,0])
pwm_bound = np.array([4])
PITCH = np.array([0])
ROLL = np.array([0])
PITCHcurr = np.array([0])
ROLLcurr = np.array([0])
OBJ = np.array([0])
init = True
init2 = True
uncontrollable_state =  27.5
stop = False

############# ROS INTEGRATION ################

import rospy
import rospkg
import os
from crazyflie_driver.msg import MotorControl, MotorControlwID, GenericLogData, LogBlock, Hover


rp = rospkg.RosPack()




x_prev = np.zeros([10])
x_prev_cached = np.zeros([10])
# x_prev_cached = np.array([-.141, -.141, -.141, 2, 3, 29, .1, -.1, 9.76,0,0,0])
x_prev_delta = np.zeros([10])
ts = np.zeros([1])
ts_cached = np.zeros([1])
pwms_cached = np.zeros([4])
pwms_received = np.zeros([4])



pwms_avg = PWMequil
controlTicks = np.zeros([1])
packet_id_rec = np.zeros([1])   # added
received = -1
generated = -1
begunReceiving = False

totalTimes = 0
totalRuns = 0
caughtRuns = 0

totalReceived = 0

# returns the elapsed milliseconds since the start of the program
def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

def clear():
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')


def callback(data):
  fetching_data = True
  begunReceiving = True
  fiftyHz = False
  global received
  received = millis()
  global totalReceived
  totalReceived += 1

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

  pwms = unpack_cf_pwm(p)
  imu = unpack_cf_imu(l,a)

  if False:
      # ypr
      ypr_p = np.zeros([1])
      ypr_p[0] = data.values[2]
      ypr = unpack_cf_ypr(ypr_p)
  else:
      ypr = np.zeros([1,3])
      ypr[0][1] = data.values[2]  #Pitch
      ypr[0][2] = data.values[3]  #Roll
      ypr[0][0] = data.values[4]  #Yaw



  # Further packed assignment
  x_prev[0] = imu[0][0]
  x_prev[1] = imu[0][1]
  x_prev[2] = imu[0][2]
  x_prev[3] = ypr[0][1] #pitch
  x_prev[4] = ypr[0][2] #roll
  x_prev[5] = ypr[0][0] #yaw
  x_prev[6] = imu[0][3] #l_x
  x_prev[7] = imu[0][4] #l_y
  x_prev[8] = imu[0][5] #l_z
  x_prev[9] = b[0]

  ts[0] = str(t)
  pwms_received[0] = pwms[0][0]
  pwms_received[1] = pwms[0][1]
  pwms_received[2] = pwms[0][2]
  pwms_received[3] = pwms[0][3]


  # packet_id_temp = np.zeros([1])
  # packet_id_temp[0] = data.values[-1]
  # packet_id_rec[0] = int(packet_id_temp[0])


  fetching_data = False

  global uncontrollable_state

  x_prev[x_prev == -90] = 0

  # if fiftyHZ:


  if ( (abs(x_prev[3]) >= uncontrollable_state) or
     (abs(x_prev[4]) >= uncontrollable_state) or
     (abs(x_prev[6])+abs(x_prev[7])  >= 10) or
     # ( <= -6) or
     (x_prev[8] <= -6) or
     (abs(x_prev_delta[0]) > 70) or
     (abs(x_prev_delta[1]) > 70) or
     (abs(x_prev_delta[2]) > 70) ):
    global stop
    stop = True



def nodecontroller():
  if logging:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    log_folder = "/home/hiro/crazyflie_ros/src/crazyflie_mpc/src/_flightlogs/_newquad1/100Hz_rand/"
    log = open(log_folder+'flight_log-'+timestr+'.csv',"w+")
    print(log)
  pub = rospy.Publisher('/cmd_vel', MotorControlwID, queue_size = 1)
  pubCont = rospy.Publisher('/cmd_hover', Hover, queue_size = 1)

  rospy.init_node('MPController', anonymous=True)
  rospy.Subscriber('/state_data', GenericLogData, callback)

  rate = rospy.Rate(100) # frequency of operation in hz
  testTime = 15000  	# Time to run realtime test, in ms

  # Take off and radio spinup flags
  take_off_flag = False
  Hop_Flag = False
  #global spinup = True

  global caughtFlag
  global caughtRuns
  global caughtTime
  global Spinup
  Spinup = True
  caughtTime = 0
  caughtFlag = False


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



################################ Obj Fnc ################################
  print('...Objective Function Initialized')

################################ MPC ####################################
  #mpc1 = MPController(newNN, crazy, dt_x, dt_u, origin_minimizer, N=100, T=5, variance = 1000)
  mpc1 = MPController(PWMequil, N=4000, T=2, variance =6000, numStack = numStack)
  print('...MPC Running')


  stopFlag = False
  plot_each = True
  takecount = 0


  pred_state = np.zeros([9])
  x_prev_stacked = np.zeros(numStack*9)
  u_prev_stacked = np.ones(numStack*4)*30000.

######################## Controller Input/Output ##################
  start_time = datetime.now()
  start_time = millis()
  x_prev_cached = np.zeros([10])
  u = np.zeros([4])

  # declare packet_id coutner
  packet_id = 0
  while  millis() < testTime:
    while not rospy.is_shutdown():

        if not fetching_data:
          x_prev_delta = x_prev - x_prev_cached
          x_prev_cached = x_prev #change from LAST state
          ts_cached = int(ts)

        msg = MotorControlwID()

############################ EMERGENCY STOP  ############################
        if stop:
          msg.m1 = 0
          msg.m2 = 0
          msg.m3 = 0
          msg.m4 = 0
          pub.publish(msg)

          print "EMERGENCY SHUTDOWN. Entered uncontrollable state: ", x_prev_cached[3], x_prev_cached[4], x_prev_cached[5]
          print x_prev_delta[0], x_prev_delta[1], x_prev_delta[2], x_prev_cached[6], x_prev_cached[7], x_prev_cached[8]

          if stopFlag:
              log.close()

              if  plot_each:
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

##################### RADIO SPINUP #######################################
        if (millis()-start_time) < spin_time:
            msg.m1 = 0
            msg.m2 = 0
            msg.m3 = 0
            msg.m4 = 0
            msg.ID = 0
            pub.publish(msg)
        else:
            Spinup = False
########################### OPEN LOOP HOP ############################
        if not take_off_flag and not Spinup and not Hop_Flag:
            mean = PWMequil

            #UNCOMMENT FOR OPEN LOOP TAKEOFF
            u[0] = mean[0] * hop_power
            u[1] = mean[1] * hop_power
            u[2] = mean[2] * hop_power
            u[3] = mean[3] * hop_power
            msg.m1 = min(max(u[0], 0), 65535)
            msg.m2 = min(max(u[1], 0), 65535)
            msg.m3 = min(max(u[2], 0), 65535)
            msg.m4 = min(max(u[3], 0), 65535)
            msg.ID = 1
            publisher(pub, msg)
            # print('HOP (RUN)')
            Hop_Flag = True
            packet_id += 1
            takecount += 1

        # if ((millis()-start_time) >= hop_time + spin_time) and not take_off_flag and not Spinup and Hop_Flag:
        #     msg.m1 = 0
        #     msg.m2 = 0
        #     msg.m3 = 0
        #     msg.m4 = 0
        #     msg.ID = 2
        #     publisher(pub, msg)
        #
        # # Update states
        # if not Spinup and Hop_Flag:
        #     # implementing for stacked states
        #
########################### OPEN LOOP TAKEOFF ############################
        if ((millis()-start_time) >= hop_delay + spin_time) and not take_off_flag and not Spinup and Hop_Flag:
            mean = PWMequil

            if not np.array_equal(x_prev_cached[:9], x_prev_stacked[:9]):
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = x_prev_cached[:9]

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = pwms_received
            else:
                print("DROPPED PACKET")
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = pred_state.cpu().detach().numpy()

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = u


            takeoff_adjust += takeoff_adjust_step
            pow = min(takeoff_power,takeoff_adjust)
            # print(pow)
            u, objval, pred_state = mpc1.update(x_prev_stacked,u_prev_stacked,pow)   # UPDATE SHOULD RETURN PWMs
            u = u[:4]

            #UNCOMMENT FOR OPEN LOOP TAKEOFF
            # u[0] = mean[0] * takeoff_power
            # u[1] = mean[1] * takeoff_power
            # u[2] = mean[2] * takeoff_power
            # u[3] = mean[3] * takeoff_power
            msg.m1 = min(max(u[0], 0), 65535)
            msg.m2 = min(max(u[1], 0), 65535)
            msg.m3 = min(max(u[2], 0), 65535)
            msg.m4 = min(max(u[3], 0), 65535)
            msg.ID = packet_id

            packet_id += 1
            takecount += 1

            publisher(pub, msg)

            print('OPEN LOOP TAKEOFF (RUN)')
            if (millis()-start_time) >= (takeoff_time + spin_time + hop_delay):
                take_off_flag = True





############################ CONTROLLED FLIGHT     ############################
        # if (millis()-start_time) <= (takeoff_time + spin_time + hop_time) and logging:
        #     log.write("{0}, {1}, {2}".format(str(x_prev_cached[3]),str(x_prev_cached[4]),str(x_prev_cached[5])))
        #     log.write('\n')

        if ((millis()-start_time) >= (takeoff_time + spin_time + hop_delay)):  #UCOMMENT FOR OPEN LOOP TAKEOFF
        # if ((millis()-start_time) >= (spin_time)):
            # if ((millis()-start_time) >= (spin_time + takeoff_time)):
            #     equilAdjust = 1.05

            if not np.array_equal(x_prev_cached[:9], x_prev_stacked[:9]):
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = x_prev_cached[:9]

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = pwms_received
            else:
                print("DROPPED PACKET")
                x_prev_stacked[9:] = x_prev_stacked[:9*(numStack-1)]
                x_prev_stacked[:9] = pred_state.cpu().detach().numpy()

                # Stacks inputs
                u_prev_stacked[4:] = u_prev_stacked[:4*(numStack-1)]
                u_prev_stacked[:4] = u

            equilAdjust = equil_step*equilAdjust
            u, objval, pred_state = mpc1.update(x_prev_stacked,u_prev_stacked,1.05)   # UPDATE SHOULD RETURN PWMs
            u = u[:4]
            OBJ[0] = objval.cpu().detach().numpy()

        if logging:
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


        generated = millis()

###################### CONSTRUCT AND SEND PACKET #############################


        if (millis()-start_time) > (hop_delay+ takeoff_time + spin_time):
        # if (millis()-start_time) > (spin_time):
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

######################################################
        global totalTimes
        global totalRuns
        totalTimes += (generated-received)
        totalRuns += 1
        rate.sleep()

        PWMdelta[:] = pwms_received[:] - PWMequil[:]
        PITCH[0] = (PWMdelta[0]+PWMdelta[3]-PWMdelta[1]- PWMdelta[2])
        ROLL[0] = (PWMdelta[2]+PWMdelta[3]-PWMdelta[0] - PWMdelta[1])
        PITCHcurr[0] = x_prev_cached[3]
        ROLLcurr[0] = x_prev_cached[4]


def publisher(pub, msg):
    pub.publish(msg)
    # print "Deltas: ", PWMdelta
    print "Roll Delta: ", ROLL, "Curr Roll: ", ROLLcurr, "Pitch Delta: ", PITCH, "Curr Pitch: ", PITCHcurr
    print "Objective: ", OBJ
    print msg.m1, msg.m2, msg.m3, msg.m4
    print "Message :", msg.ID
    print "CF PWM :" , pwms_received, "\n"
    # print "Packet ID: ", packet_id_rec, "\n"
    print "Total Radio Loop Freq Hz = ", (totalRuns / (millis() / 1000)) #Frequency control is SENT
    print "On Control Freq Hz = ", (caughtRuns /((millis()-caughtTime)/1000))



if __name__ == '__main__':
    #time.sleep(5)
  #try:
    nodecontroller()
  #except rospy.ROSInterruptExecption: pass
