; Auto-generated. Do not edit!


(cl:in-package crazyflie_driver-msg)


;//! \htmlinclude controllerFlag.msg.html

(cl:defclass <controllerFlag> (roslisp-msg-protocol:ros-message)
  ((controllerFlag
    :reader controllerFlag
    :initarg :controllerFlag
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass controllerFlag (<controllerFlag>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <controllerFlag>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'controllerFlag)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name crazyflie_driver-msg:<controllerFlag> is deprecated: use crazyflie_driver-msg:controllerFlag instead.")))

(cl:ensure-generic-function 'controllerFlag-val :lambda-list '(m))
(cl:defmethod controllerFlag-val ((m <controllerFlag>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:controllerFlag-val is deprecated.  Use crazyflie_driver-msg:controllerFlag instead.")
  (controllerFlag m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <controllerFlag>) ostream)
  "Serializes a message object of type '<controllerFlag>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'controllerFlag) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <controllerFlag>) istream)
  "Deserializes a message object of type '<controllerFlag>"
    (cl:setf (cl:slot-value msg 'controllerFlag) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<controllerFlag>)))
  "Returns string type for a message object of type '<controllerFlag>"
  "crazyflie_driver/controllerFlag")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'controllerFlag)))
  "Returns string type for a message object of type 'controllerFlag"
  "crazyflie_driver/controllerFlag")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<controllerFlag>)))
  "Returns md5sum for a message object of type '<controllerFlag>"
  "faacf4a6fc7c08bf15b15c2e29104501")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'controllerFlag)))
  "Returns md5sum for a message object of type 'controllerFlag"
  "faacf4a6fc7c08bf15b15c2e29104501")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<controllerFlag>)))
  "Returns full string definition for message of type '<controllerFlag>"
  (cl:format cl:nil "bool controllerFlag~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'controllerFlag)))
  "Returns full string definition for message of type 'controllerFlag"
  (cl:format cl:nil "bool controllerFlag~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <controllerFlag>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <controllerFlag>))
  "Converts a ROS message object to a list"
  (cl:list 'controllerFlag
    (cl:cons ':controllerFlag (controllerFlag msg))
))
