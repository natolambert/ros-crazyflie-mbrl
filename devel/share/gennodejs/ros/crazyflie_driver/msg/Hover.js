// Auto-generated. Do not edit!

// (in-package crazyflie_driver.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Hover {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.controllerFlag = null;
      this.thrust = null;
    }
    else {
      if (initObj.hasOwnProperty('controllerFlag')) {
        this.controllerFlag = initObj.controllerFlag
      }
      else {
        this.controllerFlag = false;
      }
      if (initObj.hasOwnProperty('thrust')) {
        this.thrust = initObj.thrust
      }
      else {
        this.thrust = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Hover
    // Serialize message field [controllerFlag]
    bufferOffset = _serializer.bool(obj.controllerFlag, buffer, bufferOffset);
    // Serialize message field [thrust]
    bufferOffset = _serializer.float32(obj.thrust, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Hover
    let len;
    let data = new Hover(null);
    // Deserialize message field [controllerFlag]
    data.controllerFlag = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [thrust]
    data.thrust = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'crazyflie_driver/Hover';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fe6876434232841148aa835f5a5c04aa';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool controllerFlag
    float32 thrust
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Hover(null);
    if (msg.controllerFlag !== undefined) {
      resolved.controllerFlag = msg.controllerFlag;
    }
    else {
      resolved.controllerFlag = false
    }

    if (msg.thrust !== undefined) {
      resolved.thrust = msg.thrust;
    }
    else {
      resolved.thrust = 0.0
    }

    return resolved;
    }
};

module.exports = Hover;
