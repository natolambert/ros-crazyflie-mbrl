# file for data utilities
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from datetime import timedelta
import struct

start_time = datetime.now()

def unpack_cf_pwm(packed_pwm_data):
  unpacked_pwm_data = np.zeros((len(packed_pwm_data), 4))

  packed_pwm_data_int = np.zeros(packed_pwm_data.size, dtype=int)

  for i, l in enumerate(packed_pwm_data):
    packed_pwm_data_int[i] = int(l)

  for i, packed_pwm in enumerate(packed_pwm_data_int):
    #pwms = struct.upack('4H', packed_pwm);
    #print("m1,2,3,4: ", pwms)
    m1 = ( packed_pwm        & 0xFF) << 8
    m2 = ((packed_pwm >> 8)  & 0xFF) << 8
    m3 = ((packed_pwm >> 16) & 0xFF) << 8
    m4 = ((packed_pwm >> 24) & 0xFF) << 8
    unpacked_pwm_data[i][0] = m1
    unpacked_pwm_data[i][1] = m2
    unpacked_pwm_data[i][2] = m3
    unpacked_pwm_data[i][3] = m4

  return unpacked_pwm_data

# unpacks linear and anuglar accel
def unpack_cf_imu(packed_imu_data_l, packed_imu_data_a):
  unpacked_imu_data = np.zeros((len(packed_imu_data_l), 6))

  mask = 0b1111111111

  packed_imu_data_l_int = np.zeros(packed_imu_data_l.size, dtype=int)
  packed_imu_data_a_int = np.zeros(packed_imu_data_a.size, dtype=int)

  for i, (l,a) in enumerate(zip(packed_imu_data_l, packed_imu_data_a)):
    #packed_imu_data_l_int[i] = np.uint32(l)
    #packed_imu_data_a_int[i] = np.uint32(a)
    packed_imu_data_l_int[i] = int(l)
    packed_imu_data_a_int[i] = int(a)

  for i, (packed_imu_l, packed_imu_a) in enumerate(zip(packed_imu_data_l_int, packed_imu_data_a_int)):

    lx = ( packed_imu_l        & mask)
    ly = ((packed_imu_l >> 10) & mask)
    lz = ((packed_imu_l >> 20) & mask)
    ax = ( packed_imu_a        & mask)
    ay = ((packed_imu_a >> 10) & mask)
    az = ((packed_imu_a >> 20) & mask)

    # scale back to normal (reflects values in custom cf firmware (sorry its so opaque!))
    lx = (lx / 25.6) - 20
    ly = (ly / 25.6) - 20
    lz = (lz / 25.6) - 20

    ax = (ax / 1.42)  - 360
    ay = (ay / 1.42)  - 360
    az = (az / 1.42)  - 360

    unpacked_imu_data[i][3] = lx
    unpacked_imu_data[i][4] = ly
    unpacked_imu_data[i][5] = lz
    unpacked_imu_data[i][0] = ax
    unpacked_imu_data[i][1] = ay
    unpacked_imu_data[i][2] = az

  return unpacked_imu_data

# unpacks angular accel ONLY
def unpack_cf_imu_ang(packed_imu_data_a):
  unpacked_imu_data = np.zeros((len(packed_imu_data_a), 3))

  mask = 0b1111111111
  packed_imu_data_a_int = np.zeros(packed_imu_data_a.size, dtype=int)

  for i, a in enumerate(packed_imu_data_a):
    packed_imu_data_a_int[i] = int(a)

  for i, packed_imu_a in enumerate(packed_imu_data_a_int):
    ax = ( packed_imu_a        & mask)
    ay = ((packed_imu_a >> 10) & mask)
    az = ((packed_imu_a >> 20) & mask)

    # scale back to normal (reflects values in custom cf firmware (sorry its so opaque!))
    ax = (ax / 1.42)  - 360
    ay = (ay / 1.42)  - 360
    az = (az / 1.42)  - 360

    unpacked_imu_data[i][0] = ax
    unpacked_imu_data[i][1] = ay
    unpacked_imu_data[i][2] = az

  return unpacked_imu_data


# NOL added compact YPR values
def unpack_cf_ypr(packed_ypr_data):
    unpacked_ypr = np.zeros((len(packed_ypr_data),3))

    mask = 0b1111111111

    packed_ypr_data_l_int = np.zeros(packed_ypr_data.size, dtype=int)

    for i, l in enumerate(packed_ypr_data):
        packed_ypr_data_l_int[i] = int(l)

    for i, packed_ypr_data in enumerate(packed_ypr_data_l_int):
        y = ( packed_ypr_data        & mask)
        p = ((packed_ypr_data >> 10) & mask)
        r = ((packed_ypr_data >> 20) & mask)

        y = (y / 2.84)  - 180
        p = (p / 5.68)  - 90
        r = (r / 5.68)  - 90

        unpacked_ypr[i][0] = y
        unpacked_ypr[i][1] = p
        unpacked_ypr[i][2] = r

    return unpacked_ypr
