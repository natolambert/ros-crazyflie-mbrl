#!/usr/bin/env python2.7


import torch
from torch.nn import MSELoss

from controllers import randController, MPController
from dynamics_ionocraft import IonoCraft
from dynamics_crazyflie_linearized import CrazyFlie
from dynamics import *
import numpy as np
import time

from utils_data import *

np.set_printoptions(precision=3, suppress=True, linewidth=np.nan, threshold=np.nan)

logging = False


uncontrollable_state =  60
stop = False
############# ROS INTEGRATION ################

import rospy
import rospkg
import os
from crazyflie_driver.msg import MotorControl, MotorControlwID, GenericLogData, LogBlock

rp = rospkg.RosPack()


#model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "greatmodel.pth")
model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/greatmodel-2.pth")

x_prev = np.zeros([12])
x_prev_cached = np.zeros([12])
pwms_cached = np.zeros([4])
pwms_received = np.zeros([4])
controlTicks = np.zeros([1])
packet_id_rec = np.zeros([1])   # added
received = -1
generated = -1
begunReceiving = False

totalTimes = 0
totalRuns = 0
caughtRuns = 0

totalReceived = 0

takeoff_power = 1.32
takeoff_time = 700
spin_time = 1000
fetching_data = False


def clear():
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')


def callback(data):

  ts = data.header.stamp       # note - this may be ROS time
  begunReceiving = True
  global received
  received = millis()
  global totalReceived
  totalReceived += 1
  #print "\n\n\n\ncallback hz: ", (totalReceived / (millis() * 0.001))
  #print "RECEIVED: ", data

  # pwms
  p = np.zeros([1])
  p[0] = data.values[2]

  # Linear accle
  # l = np.zeros([1])
  # l[0] = data.values[1]

  # angular accel
  a = np.zeros([1])
  a[0] = data.values[0]

  # ypr
  ypr_p = np.zeros([1])
  ypr_p[0] = data.values[1]

  pwms = unpack_cf_pwm(p)
  # controlTicks = tick[0]
  # imu = unpack_cf_imu(l,a)
  imu = unpack_cf_imu_ang(a)
  ypr = unpack_cf_ypr(ypr_p)

  fetching_data = True

  # OLD assigment
  # x_prev[0] = imu[0][3]
  # x_prev[1] = imu[0][4]
  # x_prev[2] = imu[0][5]
  # x_prev[3] = data.values[3] #pitch
  # x_prev[4] = data.values[4] #roll
  # x_prev[5] = data.values[5] #yaw

  # Further packed assignment
  x_prev[0] = imu[0][0]
  x_prev[1] = imu[0][1]
  x_prev[2] = imu[0][2]
  x_prev[3] = ypr[0][1] #pitch
  x_prev[4] = ypr[0][2] #roll
  x_prev[5] = ypr[0][0] #yaw

  pwms_received[0] = pwms[0][0]
  pwms_received[1] = pwms[0][1]
  pwms_received[2] = pwms[0][2]
  pwms_received[3] = pwms[0][3]

  packet_id_temp = np.zeros([1])
  packet_id_temp[0] = data.values[-1]
  packet_id_rec[0] = int(packet_id_temp[0])
  print "Timestamp:", ts#, ". x_prev: ", x_prev
  #if (x_prev[0] < 0) or (x_prev[1] < 0) or (x_prev[2] < 0):
  #  print "went negativer! :: ", x_prev[0], x_prev[1], x_prev[2]

  fetching_data = False
  #print "x 6 : ", x_prev[6]
  global uncontrollable_state

  x_prev[x_prev== -360] = 0
  if abs(x_prev[3]) >= uncontrollable_state or abs(x_prev[4]) >= uncontrollable_state:
    global stop
    stop = True

def callbackID(data):
    packet_id_temp = np.zeros([1])
    packet_id_temp[0] = data.values[0]
    packet_id_rec[0] = int(packet_id_temp[0])
    # print('packetID recieved in form: ', packet_id_rec)

def nodecontroller():
  if logging:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    log = open('flight_log-'+timestr+'.txt','a+')
  pub = rospy.Publisher('/cmd_vel', MotorControlwID, queue_size = 1)

  rospy.init_node('MPController', anonymous=True)
  rospy.Subscriber('/state_data', GenericLogData, callback)
  # rospy.Subscriber('/packetID', GenericLogData, callbackID)
  rate = rospy.Rate(250) # frequency of operation in hz
  testTime = 15000  	# Time to run realtime test, in ms

  # Take off and radio spinup flags
  take_off_flag = False
  spinup = True
  global caughtFlag
  global caughtRuns
  global caughtTime
  caughtTime = 0
  caughtFlag = False

############################# Get Dynamics Obj #########################

  dt_x = 0.01 # dynamics update
  dt_u = 0.01 # measurement update

  crazy = CrazyFlie(dt_x, x_noise = 0.000)

############################### Get NN Model ###########################
  print('Loading offline model')

  #torch.set_default_tensor_type('torch.cuda.FloatTensor')
  newNN = torch.load(model_path)
  #newNN = newNN.cuda()

################################ Obj Fnc ################################
  #origin_minimizer = Objective(np.linalg.norm, 'min', 6, dim_to_eval=[0,1])
  #cust_minimizer = Objective(optimizer, 'min', 5, dim_to_eval=[0,1])
  #origin_minimizer = Objective(np.linalg.norm, 'min', 3, dim_to_eval=[6,7,8])
  print('...Objective Function Initialized')

################################ MPC ####################################
  #mpc1 = MPController(newNN, crazy, dt_x, dt_u, origin_minimizer, N=100, T=5, variance = 1000)
  mpc1 = MPController(newNN, crazy, dt_x, dt_u, N=5000, T=2, variance = 5000)
  print('...MPC Running')


######################## Controller Input/Output ##################
  start_time = datetime.now()
  start_time = millis()

  # declare packet_id coutner
  packet_id = 0
  while  millis() < testTime:
    while not rospy.is_shutdown():

        if not fetching_data:
          x_prev_cached = x_prev
        time_beg = millis()

        #receieved = millis()

        # msg = MotorControl()
        msg = MotorControlwID()

        if stop:
          msg.m1 = 0
          msg.m2 = 0
          msg.m3 = 0
          msg.m4 = 0
          pub.publish(msg)
          print "EMERGENCY SHUTDOWN. Entered uncontrollable state: ", x_prev_cached[3], x_prev_cached[4], x_prev_cached[5]
          log.close()

          quit()

        # generate new u
        #u,x_predict  = mpc1.update(x_prev_cached)   # UPDATE SHOULD RETURN PWMs
        # print("x_prev: ", x_prev_cached)
        # u,pred_state  = mpc1.update(x_prev_cached)   # UPDATE SHOULD RETURN PWMs
        u  = mpc1.update(x_prev_cached)   # UPDATE SHOULD RETURN PWMs

        if logging:
          log.write(str(np.append(x_prev_cached,np.append(u,pred_state.cpu().detach().numpy()))))
        generated = millis()

        # pass new u to cf
        # Radio spinup time

        if (millis()-start_time) < spin_time:
            msg.m1 = 0
            msg.m2 = 0
            msg.m3 = 0
            msg.m4 = 0
            msg.ID = 0
        else:
            spinup = False

        # if (millis()-start_time) < takeoff_time:
        if not take_off_flag and not spinup:
            mean = mpc1.dynamics_true.u_e
            u[0] = mean[0] * takeoff_power
            u[1] = mean[1] * takeoff_power
            u[2] = mean[2] * takeoff_power
            u[3] = mean[3] * takeoff_power
            print('OPEN LOOP TAKEOFF (RUN)')

            take_off_flag = True

            msg.m1 = min(max(u[0], 0), 65535)
            msg.m2 = min(max(u[1], 0), 65535)
            msg.m3 = min(max(u[2], 0), 65535)
            msg.m4 = min(max(u[3], 0), 65535)
            msg.ID = 1
            publisher(pub, msg)
            # pub.publish(msg)
            packet_id += 1

        msg.m1 = min(max(u[0], 0), 65535)
        msg.m2 = min(max(u[1], 0), 65535)
        msg.m3 = min(max(u[2], 0), 65535)
        msg.m4 = min(max(u[3], 0), 65535)
        # Adding packet ID to PWM messages
        msg.ID = packet_id

        if (millis()-start_time) > (takeoff_time + spin_time):
            if caughtTime == 0:
                caughtTime = millis()
                caughtFlag = True
            publisher(pub, msg)
            packet_id += 1 # update packet ID on each update of control
            caughtRuns += 1

        # if ((millis()-start_time) > (spin_time + takeoff_time)) and (packet_id<50):
        #     # pub.publish(msg)
        #     publisher(pub, msg)
        #     packet_id += 1 # update packet ID on each update of control
        #     #ends as packet_id = 50
        #     global caughtTime
        #
        # elif packet_id >= 50 and not (packet_id == packet_id_rec + 1) and not caughtFlag:  #wait for packet_id_rec to catch up (should be 50)
        #     print " Packet ID: ", packet_id_rec
        #     caughtTime = millis()
        # elif packet_id >= 50 and (packet_id <= packet_id_rec + 1):
        #     caughtFlag = True
        #     publisher(pub, msg)
        #     packet_id += 1 # update packet ID on each update of control
        #     caughtRuns += 1


        #dif = np.zeros(len(x_predict[0]))
        #for i in range(0, len(x_predict[0])):
        #  dif[i] = x_prev_cached[i] - x_predict[0][i]

        global totalTimes
        global totalRuns

        totalTimes += (generated-received)
        totalRuns += 1
        #clear()
        # print "Message :\n", msg
        # print "CF PWM :\n" , pwms_received
        # print " Packet ID: ", packet_id_rec
        #print "X_Prev = \n", x_prev_cached, "\nX_Predicted = \n", x_predict, "\nDifference = \n", dif, "\nFinal Hope = \n", x_predict[2]
        #print "average error : ", np.sum(dif) / len(dif)
	# print for debugging / viewing timestamps to measure control latency and update frequ.
        #print "Received: ", received, "\nPrevious: ", x_prev, "\nGenerated: ", generated, "\nU: ", u, "\n\n\n"
        #print "Time elapsed: ", (generated-received)
        # print "Hz = ", (totalRuns / (millis() / 1000)) #Frequency control is SENT
        # print "Control ticks = ", (controlTicks)       #Frequency control is RECEIVED
        rate.sleep()

def publisher(pub, msg):
    pub.publish(msg)
    print "Message :\n", msg
    print "CF PWM :\n" , pwms_received
    print "Packet ID: ", packet_id_rec
    print "Control Update Freq Hz = ", (totalRuns / (millis() / 1000)) #Frequency control is SENT
    if (caughtFlag):
        print "On Control Freq Hz = ", (caughtRuns /((millis()-caughtTime)/1000))

if __name__ == '__main__':
    #time.sleep(5)
  #try:
    nodecontroller()
  #except rospy.ROSInterruptExecption: pass
