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

class controllerFlag {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.controllerFlag = null;
    }
    else {
      if (initObj.hasOwnProperty('controllerFlag')) {
        this.controllerFlag = initObj.controllerFlag
      }
      else {
        this.controllerFlag = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type controllerFlag
    // Serialize message field [controllerFlag]
    bufferOffset = _serializer.bool(obj.controllerFlag, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type controllerFlag
    let len;
    let data = new controllerFlag(null);
    // Deserialize message field [controllerFlag]
    data.controllerFlag = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a message object
    return 'crazyflie_driver/controllerFlag';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'faacf4a6fc7c08bf15b15c2e29104501';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool controllerFlag
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new controllerFlag(null);
    if (msg.controllerFlag !== undefined) {
      resolved.controllerFlag = msg.controllerFlag;
    }
    else {
      resolved.controllerFlag = false
    }

    return resolved;
    }
};

module.exports = controllerFlag;
