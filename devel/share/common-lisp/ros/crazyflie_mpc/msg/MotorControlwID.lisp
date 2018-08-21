; Auto-generated. Do not edit!


(cl:in-package crazyflie_mpc-msg)


;//! \htmlinclude MotorControlwID.msg.html

(cl:defclass <MotorControlwID> (roslisp-msg-protocol:ros-message)
  ((m1Motor
    :reader m1Motor
    :initarg :m1Motor
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
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name crazyflie_mpc-msg:<MotorControlwID> is deprecated: use crazyflie_mpc-msg:MotorControlwID instead.")))

(cl:ensure-generic-function 'm1Motor-val :lambda-list '(m))
(cl:defmethod m1Motor-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_mpc-msg:m1Motor-val is deprecated.  Use crazyflie_mpc-msg:m1Motor instead.")
  (m1Motor m))

(cl:ensure-generic-function 'm2-val :lambda-list '(m))
(cl:defmethod m2-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_mpc-msg:m2-val is deprecated.  Use crazyflie_mpc-msg:m2 instead.")
  (m2 m))

(cl:ensure-generic-function 'm3-val :lambda-list '(m))
(cl:defmethod m3-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_mpc-msg:m3-val is deprecated.  Use crazyflie_mpc-msg:m3 instead.")
  (m3 m))

(cl:ensure-generic-function 'm4-val :lambda-list '(m))
(cl:defmethod m4-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_mpc-msg:m4-val is deprecated.  Use crazyflie_mpc-msg:m4 instead.")
  (m4 m))

(cl:ensure-generic-function 'ID-val :lambda-list '(m))
(cl:defmethod ID-val ((m <MotorControlwID>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_mpc-msg:ID-val is deprecated.  Use crazyflie_mpc-msg:ID instead.")
  (ID m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MotorControlwID>) ostream)
  "Serializes a message object of type '<MotorControlwID>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm1Motor)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm1Motor)) ostream)
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
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'm1Motor)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'm1Motor)) (cl:read-byte istream))
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
  "crazyflie_mpc/MotorControlwID")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MotorControlwID)))
  "Returns string type for a message object of type 'MotorControlwID"
  "crazyflie_mpc/MotorControlwID")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MotorControlwID>)))
  "Returns md5sum for a message object of type '<MotorControlwID>"
  "53816296b5bd669972d937c31e11fb61")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MotorControlwID)))
  "Returns md5sum for a message object of type 'MotorControlwID"
  "53816296b5bd669972d937c31e11fb61")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MotorControlwID>)))
  "Returns full string definition for message of type '<MotorControlwID>"
  (cl:format cl:nil "uint16 m1Motor~%uint16 m2~%uint16 m3~%uint16 m4~%uint16 ID~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MotorControlwID)))
  "Returns full string definition for message of type 'MotorControlwID"
  (cl:format cl:nil "uint16 m1Motor~%uint16 m2~%uint16 m3~%uint16 m4~%uint16 ID~%~%~%"))
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
    (cl:cons ':m1Motor (m1Motor msg))
    (cl:cons ':m2 (m2 msg))
    (cl:cons ':m3 (m3 msg))
    (cl:cons ':m4 (m4 msg))
    (cl:cons ':ID (ID msg))
))
