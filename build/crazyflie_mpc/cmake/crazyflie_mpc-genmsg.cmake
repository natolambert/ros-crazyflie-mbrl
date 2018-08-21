# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "crazyflie_mpc: 4 messages, 0 services")

set(MSG_I_FLAGS "-Icrazyflie_mpc:/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(crazyflie_mpc_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_custom_target(_crazyflie_mpc_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "crazyflie_mpc" "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" ""
)

get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_custom_target(_crazyflie_mpc_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "crazyflie_mpc" "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" ""
)

get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_custom_target(_crazyflie_mpc_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "crazyflie_mpc" "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_custom_target(_crazyflie_mpc_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "crazyflie_mpc" "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_cpp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_cpp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_cpp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
)

### Generating Services

### Generating Module File
_generate_module_cpp(crazyflie_mpc
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(crazyflie_mpc_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(crazyflie_mpc_generate_messages crazyflie_mpc_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_cpp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_cpp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_cpp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_cpp _crazyflie_mpc_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(crazyflie_mpc_gencpp)
add_dependencies(crazyflie_mpc_gencpp crazyflie_mpc_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS crazyflie_mpc_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_eus(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_eus(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_eus(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
)

### Generating Services

### Generating Module File
_generate_module_eus(crazyflie_mpc
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(crazyflie_mpc_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(crazyflie_mpc_generate_messages crazyflie_mpc_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_eus _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_eus _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_eus _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_eus _crazyflie_mpc_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(crazyflie_mpc_geneus)
add_dependencies(crazyflie_mpc_geneus crazyflie_mpc_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS crazyflie_mpc_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_lisp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_lisp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_lisp(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
)

### Generating Services

### Generating Module File
_generate_module_lisp(crazyflie_mpc
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(crazyflie_mpc_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(crazyflie_mpc_generate_messages crazyflie_mpc_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_lisp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_lisp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_lisp _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_lisp _crazyflie_mpc_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(crazyflie_mpc_genlisp)
add_dependencies(crazyflie_mpc_genlisp crazyflie_mpc_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS crazyflie_mpc_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_nodejs(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_nodejs(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_nodejs(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
)

### Generating Services

### Generating Module File
_generate_module_nodejs(crazyflie_mpc
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(crazyflie_mpc_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(crazyflie_mpc_generate_messages crazyflie_mpc_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_nodejs _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_nodejs _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_nodejs _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_nodejs _crazyflie_mpc_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(crazyflie_mpc_gennodejs)
add_dependencies(crazyflie_mpc_gennodejs crazyflie_mpc_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS crazyflie_mpc_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_py(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_py(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
)
_generate_msg_py(crazyflie_mpc
  "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
)

### Generating Services

### Generating Module File
_generate_module_py(crazyflie_mpc
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(crazyflie_mpc_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(crazyflie_mpc_generate_messages crazyflie_mpc_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControlwID.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_py _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/LogBlock.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_py _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/GenericLogData.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_py _crazyflie_mpc_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/hiro/crazyflie_ros/src/crazyflie_mpc/msg/MotorControl.msg" NAME_WE)
add_dependencies(crazyflie_mpc_generate_messages_py _crazyflie_mpc_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(crazyflie_mpc_genpy)
add_dependencies(crazyflie_mpc_genpy crazyflie_mpc_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS crazyflie_mpc_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/crazyflie_mpc
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(crazyflie_mpc_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/crazyflie_mpc
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(crazyflie_mpc_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/crazyflie_mpc
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(crazyflie_mpc_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/crazyflie_mpc
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(crazyflie_mpc_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/crazyflie_mpc
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(crazyflie_mpc_generate_messages_py std_msgs_generate_messages_py)
endif()
