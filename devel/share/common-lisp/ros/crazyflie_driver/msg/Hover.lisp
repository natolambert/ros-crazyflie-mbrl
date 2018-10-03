; Auto-generated. Do not edit!


(cl:in-package crazyflie_driver-msg)


;//! \htmlinclude Hover.msg.html

(cl:defclass <Hover> (roslisp-msg-protocol:ros-message)
  ((controllerFlag
    :reader controllerFlag
    :initarg :controllerFlag
    :type cl:boolean
    :initform cl:nil)
   (thrust
    :reader thrust
    :initarg :thrust
    :type cl:float
    :initform 0.0))
)

(cl:defclass Hover (<Hover>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Hover>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Hover)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name crazyflie_driver-msg:<Hover> is deprecated: use crazyflie_driver-msg:Hover instead.")))

(cl:ensure-generic-function 'controllerFlag-val :lambda-list '(m))
(cl:defmethod controllerFlag-val ((m <Hover>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:controllerFlag-val is deprecated.  Use crazyflie_driver-msg:controllerFlag instead.")
  (controllerFlag m))

(cl:ensure-generic-function 'thrust-val :lambda-list '(m))
(cl:defmethod thrust-val ((m <Hover>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader crazyflie_driver-msg:thrust-val is deprecated.  Use crazyflie_driver-msg:thrust instead.")
  (thrust m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Hover>) ostream)
  "Serializes a message object of type '<Hover>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'controllerFlag) 1 0)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'thrust))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Hover>) istream)
  "Deserializes a message object of type '<Hover>"
    (cl:setf (cl:slot-value msg 'controllerFlag) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'thrust) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Hover>)))
  "Returns string type for a message object of type '<Hover>"
  "crazyflie_driver/Hover")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Hover)))
  "Returns string type for a message object of type 'Hover"
  "crazyflie_driver/Hover")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Hover>)))
  "Returns md5sum for a message object of type '<Hover>"
  "fe6876434232841148aa835f5a5c04aa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Hover)))
  "Returns md5sum for a message object of type 'Hover"
  "fe6876434232841148aa835f5a5c04aa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Hover>)))
  "Returns full string definition for message of type '<Hover>"
  (cl:format cl:nil "bool controllerFlag~%float32 thrust~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Hover)))
  "Returns full string definition for message of type 'Hover"
  (cl:format cl:nil "bool controllerFlag~%float32 thrust~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Hover>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Hover>))
  "Converts a ROS message object to a list"
  (cl:list 'Hover
    (cl:cons ':controllerFlag (controllerFlag msg))
    (cl:cons ':thrust (thrust msg))
))
