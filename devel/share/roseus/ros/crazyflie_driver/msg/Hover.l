;; Auto-generated. Do not edit!


(when (boundp 'crazyflie_driver::Hover)
  (if (not (find-package "CRAZYFLIE_DRIVER"))
    (make-package "CRAZYFLIE_DRIVER"))
  (shadow 'Hover (find-package "CRAZYFLIE_DRIVER")))
(unless (find-package "CRAZYFLIE_DRIVER::HOVER")
  (make-package "CRAZYFLIE_DRIVER::HOVER"))

(in-package "ROS")
;;//! \htmlinclude Hover.msg.html


(defclass crazyflie_driver::Hover
  :super ros::object
  :slots (_controllerFlag _thrust ))

(defmethod crazyflie_driver::Hover
  (:init
   (&key
    ((:controllerFlag __controllerFlag) nil)
    ((:thrust __thrust) 0.0)
    )
   (send-super :init)
   (setq _controllerFlag __controllerFlag)
   (setq _thrust (float __thrust))
   self)
  (:controllerFlag
   (&optional __controllerFlag)
   (if __controllerFlag (setq _controllerFlag __controllerFlag)) _controllerFlag)
  (:thrust
   (&optional __thrust)
   (if __thrust (setq _thrust __thrust)) _thrust)
  (:serialization-length
   ()
   (+
    ;; bool _controllerFlag
    1
    ;; float32 _thrust
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _controllerFlag
       (if _controllerFlag (write-byte -1 s) (write-byte 0 s))
     ;; float32 _thrust
       (sys::poke _thrust (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _controllerFlag
     (setq _controllerFlag (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float32 _thrust
     (setq _thrust (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get crazyflie_driver::Hover :md5sum-) "fe6876434232841148aa835f5a5c04aa")
(setf (get crazyflie_driver::Hover :datatype-) "crazyflie_driver/Hover")
(setf (get crazyflie_driver::Hover :definition-)
      "bool controllerFlag
float32 thrust

")



(provide :crazyflie_driver/Hover "fe6876434232841148aa835f5a5c04aa")


