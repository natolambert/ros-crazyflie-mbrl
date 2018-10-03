#!/usr/bin/env python2.7


import torch
from torch.nn import MSELoss

from controllers import randController, MPController
from dynamics_ionocraft import IonoCraft
from dynamics_crazyflie_linearized import CrazyFlie
from dynamics import *
import numpy as np
import time
import matplotlib.pyplot as plt
from utils_data import *

np.set_printoptions(precision=3, suppress=True, linewidth=np.nan, threshold=np.nan)

logging = True


PWMequil = np.array([43512,44000,42422,39453])
PWMequil = np.array([44987,	40394,	50632,	37533])
PWMequil = np.array([46995,	41017,	47951,	38337])
PWMequil = np.array([47720,	42120,	49013,	38642])
PWMequil = np.array([37134,	34667,	37017,	33483])   # NO PROP GAURD
PWMequil = np.array([36334.,	36847.,	39682.,	33483.])
# np.array([56261, 51305, 58112, 47324])
PWMdelta = np.array([0,0,0,0])
pwm_bound = np.array([4])
PITCH = np.array([0])
ROLL = np.array([0])
PITCHcurr = np.array([0])
ROLLcurr = np.array([0])
OBJ = np.array([0])
init = True
init2 = True
uncontrollable_state =  32
stop = False
############# ROS INTEGRATION ################

import rospy
import rospkg
import os
from crazyflie_driver.msg import MotorControl, MotorControlwID, GenericLogData, LogBlock

rp = rospkg.RosPack()


#model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "greatmodel.pth")
# model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/current2018-09-07--16-11-12.3--Min error0.035589433410792674||w=500e=360lr=0.001b=20de=3d=_SEP6p=False_best/2018-08-23--14-21-35.9||w=150e=250lr=7e-06b=32d=2018_08_22_cf1_hover_p=True.pth")
model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/sep12_float/2018-09-12--18-56-18.5--Min error0.0001074432409094537--w=500e=250lr=0.001b=32de=3d=_CONF_p=True.pth")
# old greatmodel-2.pth

# Models used in rollout Aug 31st
# 0: current_best/2018-08-29--07-19-20.1||w=150e=360lr=2.5e-05b=50de=3d=2018_08_22_cf1_activeflight_p=True
# 1: current_best/2018-08-31--13-23-33.6||w=150e=300lr=5e-05b=150de=3d=_AUG29_125RL2p=True.pth
# 2: current_best/2018-08-31--13-47-42.2||w=150e=300lr=5e-05b=150de=3d=_AUG31_125RLp=True
# 3: current_best/2018-08-31--14-16-53.7||w=150e=300lr=5e-05b=150de=3d=_AUG31_125RLp=True.pth
x_prev = np.zeros([12])
x_prev_cached = np.zeros([12])
# x_prev_cached = np.array([-.141, -.141, -.141, 2, 3, 29, .1, -.1, 9.76,0,0,0])
x_prev_delta = np.zeros([12])
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

takeoff_power = 1.6
takeoff_time = 250
spin_time = 250
fetching_data = False

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

  begunReceiving = True
  global received
  received = millis()
  global totalReceived
  totalReceived += 1
  #print "\n\n\n\ncallback hz: ", (totalReceived / (millis() * 0.001))
  #print "RECEIVED: ", data

  # ts = np.zeros([1])
  t = data.header.stamp       # note - this may be ROS time

  # pwms
  p = np.zeros([1])
  p[0] = data.values[-2]

  # Linear accle
  l = np.zeros([1])
  l[0] = data.values[1]

  # angular accel
  a = np.zeros([1])
  a[0] = data.values[0]



  pwms = unpack_cf_pwm(p)
  # controlTicks = tick[0]
  imu = unpack_cf_imu(l,a)
  # imu = unpack_cf_imu_ang(a)
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
  x_prev[6] = imu[0][3] #l_x
  x_prev[7] = imu[0][4] #l_y
  x_prev[8] = imu[0][5] #l_z
  # print(x_prev[8])

  ts[0] = str(t)
  pwms_received[0] = pwms[0][0]
  pwms_received[1] = pwms[0][1]
  pwms_received[2] = pwms[0][2]
  pwms_received[3] = pwms[0][3]

  packet_id_temp = np.zeros([1])
  packet_id_temp[0] = data.values[-1]
  packet_id_rec[0] = int(packet_id_temp[0])
  # print "Timestamp:", t, ". x_prev: ", x_prev
  #if (x_prev[0] < 0) or (x_prev[1] < 0) or (x_prev[2] < 0):
  #  print "went negativer! :: ", x_prev[0], x_prev[1], x_prev[2]

  fetching_data = False
  #print "x 6 : ", x_prev[6]
  global uncontrollable_state
  # print(x_prev)
  x_prev[x_prev == -90] = 0
  # print(x_prev)
  if ( (abs(x_prev[3]) >= uncontrollable_state) or
     (abs(x_prev[4]) >= uncontrollable_state) or
     (abs(x_prev[6])+abs(x_prev[7])  >= 15) or
     # ( <= -6) or
     (x_prev[8] <= -6) or
     (abs(x_prev_delta[0]) > 70) or
     (abs(x_prev_delta[1]) > 70) or
     (abs(x_prev_delta[2]) > 70) ):
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
    log_folder = "/home/hiro/crazyflie_ros/src/crazyflie_mpc/src/_flightlogs/50Hz_1/"
    log = open(log_folder+'flight_log-'+timestr+'.csv',"w+")
    print(log)
  pub = rospy.Publisher('/cmd_vel', MotorControlwID, queue_size = 1)

  rospy.init_node('MPController', anonymous=True)
  rospy.Subscriber('/state_data', GenericLogData, callback)
  # rospy.Subscriber('/packetID', GenericLogData, callbackID)
  rate = rospy.Rate(50) # frequency of operation in hz
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
  mpc1 = MPController(newNN, crazy, dt_x, dt_u, N=1000, T=3, variance = 5000)
  print('...MPC Running')

  init = True
  init2 = True
  init3 = True
  stopFlag = False
  plot_each = True
  takecount = 0
  pwms_avg = 1.05*PWMequil
  stack = 2
  x_prev_stacked = np.array([0,0,0,0,0,0,0,0,9.76,0,0,0,0,0,0,0,0,0]) #np.zeros(stack*9)
######################## Controller Input/Output ##################
  start_time = datetime.now()
  start_time = millis()
  x_prev_cached = np.zeros([12])
  # x_prev_cached = np.array([-.141, -.141, -.141, 2, 3, 29, .1, -.1, 9.76,0,0,0])

  # declare packet_id coutner
  packet_id = 0
  while  millis() < testTime:
    while not rospy.is_shutdown():

        if not fetching_data:
          x_prev_delta = x_prev - x_prev_cached
          x_prev_cached = x_prev
          ts_cached = int(ts)


        # msg = MotorControl()
        msg = MotorControlwID()

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
                      ax1.legend()
                      ax1.set_title('FLIGHT PWMS / EULER')
                      ax1.set_xlabel('PACKET NUMBER')
                      ax1.set_ylabel("PWM VALUES")

                      # plot euler angles
                      ax2 = plt.subplot(212)
                      ax2.plot(Euler[:,0], label='PITCH')
                      ax2.plot(Euler[:,1], label='ROLL')
                      ax2.legend()
                      ax2.set_xlabel('PACKET NUMBER')
                      ax2.set_ylabel("EULER ANGLES (DEG)")

                      plt.savefig("flightplots/"+timestr)
                      # plt.show()

              quit()

          stopFlag= True


        # generate new u
        #u,x_predict  = mpc1.update(x_prev_cached)   # UPDATE SHOULD RETURN PWMs
        # print("x_prev: ", x_prev_cached)
        # u,pred_state  = mpc1.update(x_prev_cached)   # UPDATE SHOULD RETURN PWMs
        if ((millis()-start_time) >= (takeoff_time +spin_time)) and init:
            # u, objval = mpc1.update(x_prev_cached,1.*PWMequil)   # UPDATE SHOULD RETURN PWMs

            # implementing for stacked states
            x_prev_stacked[9:] = x_prev_stacked[:9]
            x_prev_stacked[:9] = x_prev_cached[:9]
            u, objval = mpc1.update(x_prev_stacked,1.*PWMequil)   # UPDATE SHOULD RETURN PWMs
            if init2:
                init2 = False
            else:
                if init3:
                    init3 = False
                else:
                    init = False
        else:
            # navg = 10
            # pwms_avg = (pwms_received/navg) + ((navg-1)*pwms_avg/navg)
            # pwm_bound = [min(55000,max(30000,i)) for i in pwms_received]
            # u, objval = mpc1.update(x_prev_cached,PWMequil) #pwm_bound)   # UPDATE SHOULD RETURN PWMs

            # implementing for stacked states
            x_prev_stacked[9:] = x_prev_stacked[:9]
            x_prev_stacked[:9] = x_prev_cached[:9]
            # x_prev_stacked = np.random.normal(0,1,18)*[30,30,30,10,10,10,1,1,1,30,30,30,10,10,10,1,1,1,]+[0,0,0,0,0,0,0,0,9.76,0,0,0,0,0,0,0,0,9.76]

            # u, objval = mpc1.update(x_prev_stacked,pwms_received) #pwm_bound)   # UPDATE SHOULD RETURN PWMs
            u, objval = mpc1.update(x_prev_stacked,1.*PWMequil) #pwm_bound)   # UPDATE SHOULD RETURN PWMs

        u = u[:4]

        #print objval.cpu().detach().numpy()
        OBJ[0] = objval.cpu().detach().numpy()

        if logging and ((millis()-start_time) > (takeoff_time + spin_time)):
          # print('write!')

          # logs the sate data, inputs, and time stampe with current object function
          # Log angular accels and YPR
          log.write("{0},{1},{2},{3},{4},{5},".format(str(x_prev_cached[0]),str(x_prev_cached[1]),str(x_prev_cached[2]),str(x_prev_cached[3]),str(x_prev_cached[4]),str(x_prev_cached[5])))
          # Log raw lienar accel`
          log.write("{0},{1},{2},".format(str(x_prev_cached[6]),str(x_prev_cached[7]),str(x_prev_cached[8])))

          # log past PWM values
          log.write("{0},{1},{2},{3},".format(pwms_received[0],pwms_received[1],pwms_received[2],pwms_received[3]))

          # Log time stamp
          log.write("{0},{1}".format(str(ts_cached),str(objval.cpu().detach().numpy())))
          # str(np.append(x_prev_cached,np.append(u,np.append(ts_cached,objval.cpu().detach().numpy())))))
          log.write('\n')
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
        if (not take_off_flag and not spinup):# or takecount < 5:
            mean = mpc1.dynamics_true.u_e
            u[0] = mean[0] * takeoff_power
            u[1] = mean[1] * takeoff_power
            u[2] = mean[2] * takeoff_power
            u[3] = mean[3] * takeoff_power
            print('OPEN LOOP TAKEOFF (RUN)')
            # print takecount
            # if takecount == 4:
            #     take_off_flag = True
            #     print('done')
            take_off_flag = True

            msg.m1 = min(max(u[0], 0), 65535)
            msg.m2 = min(max(u[1], 0), 65535)
            msg.m3 = min(max(u[2], 0), 65535)
            msg.m4 = min(max(u[3], 0), 65535)
            msg.ID = 1

            publisher(pub, msg)
            # pub.publish(msg)
            packet_id += 1
            takecount += 1

        #
        # u[0] +=  -256
        # u[3] += 0
        # u[1] +=  512+ 1024
        # u[2] += 512
        PWMdelta[:] = pwms_received[:] - PWMequil[:]
        PITCH[0] = (PWMdelta[0]+PWMdelta[3]-PWMdelta[1]- PWMdelta[2])
        ROLL[0] = (PWMdelta[2]+PWMdelta[3]-PWMdelta[0] - PWMdelta[1])
        PITCHcurr[0] = x_prev_cached[3]
        ROLLcurr[0] = x_prev_cached[4]
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
    # print "Deltas: ", PWMdelta
    print "Roll Delta: ", ROLL, "Curr Roll: ", ROLLcurr, "Pitch Delta: ", PITCH, "Curr Pitch: ", PITCHcurr
    print "Objective: ", OBJ
    print "Message :", msg.ID
    print "CF PWM :" , pwms_received, "\n"
    print "Packet ID: ", packet_id_rec, "\n"
    print "Control Update Freq Hz = ", (totalRuns / (millis() / 1000)) #Frequency control is SENT
    if (caughtFlag):
        print "On Control Freq Hz = ", (caughtRuns /((millis()-caughtTime)/1000))

if __name__ == '__main__':
    #time.sleep(5)
  #try:
    nodecontroller()
  #except rospy.ROSInterruptExecption: pass
