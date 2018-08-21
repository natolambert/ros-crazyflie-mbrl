;; Auto-generated. Do not edit!


(when (boundp 'crazyflie_mpc::MotorControlwID)
  (if (not (find-package "CRAZYFLIE_MPC"))
    (make-package "CRAZYFLIE_MPC"))
  (shadow 'MotorControlwID (find-package "CRAZYFLIE_MPC")))
(unless (find-package "CRAZYFLIE_MPC::MOTORCONTROLWID")
  (make-package "CRAZYFLIE_MPC::MOTORCONTROLWID"))

(in-package "ROS")
;;//! \htmlinclude MotorControlwID.msg.html


(defclass crazyflie_mpc::MotorControlwID
  :super ros::object
  :slots (_m1Motor _m2 _m3 _m4 _ID ))

(defmethod crazyflie_mpc::MotorControlwID
  (:init
   (&key
    ((:m1Motor __m1Motor) 0)
    ((:m2 __m2) 0)
    ((:m3 __m3) 0)
    ((:m4 __m4) 0)
    ((:ID __ID) 0)
    )
   (send-super :init)
   (setq _m1Motor (round __m1Motor))
   (setq _m2 (round __m2))
   (setq _m3 (round __m3))
   (setq _m4 (round __m4))
   (setq _ID (round __ID))
   self)
  (:m1Motor
   (&optional __m1Motor)
   (if __m1Motor (setq _m1Motor __m1Motor)) _m1Motor)
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
    ;; uint16 _m1Motor
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
     ;; uint16 _m1Motor
       (write-word _m1Motor s)
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
   ;; uint16 _m1Motor
     (setq _m1Motor (sys::peek buf ptr- :short)) (incf ptr- 2)
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

(setf (get crazyflie_mpc::MotorControlwID :md5sum-) "53816296b5bd669972d937c31e11fb61")
(setf (get crazyflie_mpc::MotorControlwID :datatype-) "crazyflie_mpc/MotorControlwID")
(setf (get crazyflie_mpc::MotorControlwID :definition-)
      "uint16 m1Motor
uint16 m2
uint16 m3
uint16 m4
uint16 ID

")



(provide :crazyflie_mpc/MotorControlwID "53816296b5bd669972d937c31e11fb61")


