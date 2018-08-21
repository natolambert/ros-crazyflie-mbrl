;; Auto-generated. Do not edit!


(when (boundp 'crazyflie_driver::MotorControlwID)
  (if (not (find-package "CRAZYFLIE_DRIVER"))
    (make-package "CRAZYFLIE_DRIVER"))
  (shadow 'MotorControlwID (find-package "CRAZYFLIE_DRIVER")))
(unless (find-package "CRAZYFLIE_DRIVER::MOTORCONTROLWID")
  (make-package "CRAZYFLIE_DRIVER::MOTORCONTROLWID"))

(in-package "ROS")
;;//! \htmlinclude MotorControlwID.msg.html


(defclass crazyflie_driver::MotorControlwID
  :super ros::object
  :slots (_m1 _m2 _m3 _m4 _ID ))

(defmethod crazyflie_driver::MotorControlwID
  (:init
   (&key
    ((:m1 __m1) 0)
    ((:m2 __m2) 0)
    ((:m3 __m3) 0)
    ((:m4 __m4) 0)
    ((:ID __ID) 0)
    )
   (send-super :init)
   (setq _m1 (round __m1))
   (setq _m2 (round __m2))
   (setq _m3 (round __m3))
   (setq _m4 (round __m4))
   (setq _ID (round __ID))
   self)
  (:m1
   (&optional __m1)
   (if __m1 (setq _m1 __m1)) _m1)
  (:m2
   (&optional __m2)
   (if __m2 (setq _m2 __m2)) _m2)
  (:m3
   (&optional __m3)
   (if __m3 (setq _m3 __m3)) _m3)
  (:m4
   (&optional __m4)
   (if __m4 (setq _m4 __m4)) _m4)
  (:ID
   (&optional __ID)
   (if __ID (setq _ID __ID)) _ID)
  (:serialization-length
   ()
   (+
    ;; uint16 _m1
    2
    ;; uint16 _m2
    2
    ;; uint16 _m3
    2
    ;; uint16 _m4
    2
    ;; uint16 _ID
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _m1
       (write-word _m1 s)
     ;; uint16 _m2
       (write-word _m2 s)
     ;; uint16 _m3
       (write-word _m3 s)
     ;; uint16 _m4
       (write-word _m4 s)
     ;; uint16 _ID
       (write-word _ID s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _m1
     (setq _m1 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _m2
     (setq _m2 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _m3
     (setq _m3 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _m4
     (setq _m4 (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint16 _ID
     (setq _ID (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get crazyflie_driver::MotorControlwID :md5sum-) "df11cfbc0178ba6af8c99c3ea9325b85")
(setf (get crazyflie_driver::MotorControlwID :datatype-) "crazyflie_driver/MotorControlwID")
(setf (get crazyflie_driver::MotorControlwID :definition-)
      "uint16 m1
uint16 m2
uint16 m3
uint16 m4
uint16 ID

")



(provide :crazyflie_driver/MotorControlwID "df11cfbc0178ba6af8c99c3ea9325b85")


