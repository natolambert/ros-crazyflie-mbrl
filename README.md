crazyflie_ros-pwm-control
=============

This is a working ROS directory for controlling a Crazyflie with Crazyradio PA. We added a directory to the src called /crazyflie_mpc/ that holds the launch files and scripts needed to run. The scripts that do the most of the work are MPController.py and rundynamics_stacked.py. These create a ROS node that subscribes to state data and sends controls from the model predictive controller running on a Nvidia Titan.

Usage Instructions
------------------

Clone the package into your catkin workspace:
```
git clone https://github.com/natolambert/crazyflie-ros-mbrl.git
cd crazyflie_ros
```

Use `catkin_make` on your workspace to compile.

To build and run:
```
./run.bash
```
If you have issues running, check the run.bash script. You may need to change the joy_dev location or crazyflie uri.

For more information, look at the readme for https://github.com/whoenig/crazyflie_ros.git
Most of it will still pertain to this project.

Control messages are published to the /crazyflie/cmd_vel topic in the form of /crazyflie_driver/MotorControl messages:
```
uint16 m1
uint16 m2
uint16 m3
uint16 m4
```

Intended for use in conjunction with https://github.com/natolambert/crazyflie-firmware-pwm-control.

The implementation of potential note is the cuda MPC implementation in crazyflie_mpc directory. We achieve > 150Hz control frequency with a nueral network dynamics model by parallelization on a Nvidia titan XP.

