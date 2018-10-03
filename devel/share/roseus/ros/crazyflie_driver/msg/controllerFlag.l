;; Auto-generated. Do not edit!


(when (boundp 'crazyflie_driver::controllerFlag)
  (if (not (find-package "CRAZYFLIE_DRIVER"))
    (make-package "CRAZYFLIE_DRIVER"))
  (shadow 'controllerFlag (find-package "CRAZYFLIE_DRIVER")))
(unless (find-package "CRAZYFLIE_DRIVER::CONTROLLERFLAG")
  (make-package "CRAZYFLIE_DRIVER::CONTROLLERFLAG"))

(in-package "ROS")
;;//! \htmlinclude controllerFlag.msg.html


(defclass crazyflie_driver::controllerFlag
  :super ros::object
  :slots (_controllerFlag ))

(defmethod crazyflie_driver::controllerFlag
  (:init
   (&key
    ((:controllerFlag __controllerFlag) nil)
    )
   (send-super :init)
   (setq _controllerFlag __controllerFlag)
   self)
  (:controllerFlag
   (&optional __controllerFlag)
   (if __controllerFlag (setq _controllerFlag __controllerFlag)) _controllerFlag)
  (:serialization-length
   ()
   (+
    ;; bool _controllerFlag
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _controllerFlag
       (if _controllerFlag (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _controllerFlag
     (setq _controllerFlag (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get crazyflie_driver::controllerFlag :md5sum-) "faacf4a6fc7c08bf15b15c2e29104501")
(setf (get crazyflie_driver::controllerFlag :datatype-) "crazyflie_driver/controllerFlag")
(setf (get crazyflie_driver::controllerFlag :definition-)
      "bool controllerFlag

")



(provide :crazyflie_driver/controllerFlag "faacf4a6fc7c08bf15b15c2e29104501")


