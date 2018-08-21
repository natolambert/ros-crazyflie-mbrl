; Auto-generated. Do not edit!


(cl:in-package crazyflie_driver-msg)


;//! \htmlinclude MotorControlwID.msg.html

(cl:defclass <MotorControlwID> (roslisp-msg-protocol:ros-message)
  ((m1
    :reader m1
    :initarg :m1
    :type cl:fixnum
    :initform 0)
   (m2
    :reader m2
    :initarg :m2
    :type cl:fixnum
    :initform 0)
   (m3
    :reader m3
    :initarg :m3
    :type cl:fixnum
    :initform 0)
   (m4
    :reader m4
    :initarg :m4
    :type cl:fixnum
    :initform 0)
   (ID
    :reader ID
    :initarg :ID
    :type cl:fixnum
    :initform 0))
)

(cl:defclass MotorControlwID (<MotorControlwID>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MotorControlwID>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MotorControlwID)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name crazyflie_driver-msg:<MotorControlwID> is deprecated: use crazyflie_driver-msg:MotorControlwID instead.")))

(cl:ensure-generic-function 'm1-val :lambda-list '(m))
(cl:defmethod m1-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:m1-val is deprecated.  Use crazyflie_driver-msg:m1 instead.")
  (m1 m))

(cl:ensure-generic-function 'm2-val :lambda-list '(m))
(cl:defmethod m2-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:m2-val is deprecated.  Use crazyflie_driver-msg:m2 instead.")
  (m2 m))

(cl:ensure-generic-function 'm3-val :lambda-list '(m))
(cl:defmethod m3-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:m3-val is deprecated.  Use crazyflie_driver-msg:m3 instead.")
  (m3 m))

(cl:ensure-generic-function 'm4-val :lambda-list '(m))
(cl:defmethod m4-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:m4-val is deprecated.  Use crazyflie_driver-msg:m4 instead.")
  (m4 m))

(cl:ensure-generic-function 'ID-val :lambda-list '(m))
(cl:defmethod ID-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:ID-val is deprecated.  Use crazyflie_driver-msg:ID instead.")
  (ID m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MotorControlwID>) ostream)
  "Serializes a message object of type '<MotorControlwID>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm1)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm1)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm2)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm2)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm3)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm3)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm4)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm4)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ID)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'ID)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MotorControlwID>) istream)
  "Deserializes a message object of type '<MotorControlwID>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm1)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm1)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm2)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm2)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm3)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm3)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm4)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm4)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ID)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'ID)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MotorControlwID>)))
  "Returns string type for a message object of type '<MotorControlwID>"
  "crazyflie_driver/MotorControlwID")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MotorControlwID)))
  "Returns string type for a message object of type 'MotorControlwID"
  "crazyflie_driver/MotorControlwID")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MotorControlwID>)))
  "Returns md5sum for a message object of type '<MotorControlwID>"
  "df11cfbc0178ba6af8c99c3ea9325b85")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MotorControlwID)))
  "Returns md5sum for a message object of type 'MotorControlwID"
  "df11cfbc0178ba6af8c99c3ea9325b85")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MotorControlwID>)))
  "Returns full string definition for message of type '<MotorControlwID>"
  (cl:format cl:nil "uint16 m1~%uint16 m2~%uint16 m3~%uint16 m4~%uint16 ID~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MotorControlwID)))
  "Returns full string definition for message of type 'MotorControlwID"
  (cl:format cl:nil "uint16 m1~%uint16 m2~%uint16 m3~%uint16 m4~%uint16 ID~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MotorControlwID>))
  (cl:+ 0
     2
     2
     2
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MotorControlwID>))
  "Converts a ROS message object to a list"
  (cl:list 'MotorControlwID
    (cl:cons ':m1 (m1 msg))
    (cl:cons ':m2 (m2 msg))
    (cl:cons ':m3 (m3 msg))
    (cl:cons ':m4 (m4 msg))
    (cl:cons ':ID (ID msg))
))
