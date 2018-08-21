// Auto-generated. Do not edit!

// (in-package crazyflie_mpc.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class MotorControlwID {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.m1Motor = null;
      this.m2 = null;
      this.m3 = null;
      this.m4 = null;
      this.ID = null;
    }
    else {
      if (initObj.hasOwnProperty('m1Motor')) {
        this.m1Motor = initObj.m1Motor
      }
      else {
        this.m1Motor = 0;
      }
      if (initObj.hasOwnProperty('m2')) {
        this.m2 = initObj.m2
      }
      else {
        this.m2 = 0;
      }
      if (initObj.hasOwnProperty('m3')) {
        this.m3 = initObj.m3
      }
      else {
        this.m3 = 0;
      }
      if (initObj.hasOwnProperty('m4')) {
        this.m4 = initObj.m4
      }
      else {
        this.m4 = 0;
      }
      if (initObj.hasOwnProperty('ID')) {
        this.ID = initObj.ID
      }
      else {
        this.ID = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MotorControlwID
    // Serialize message field [m1Motor]
    bufferOffset = _serializer.uint16(obj.m1Motor, buffer, bufferOffset);
    // Serialize message field [m2]
    bufferOffset = _serializer.uint16(obj.m2, buffer, bufferOffset);
    // Serialize message field [m3]
    bufferOffset = _serializer.uint16(obj.m3, buffer, bufferOffset);
    // Serialize message field [m4]
    bufferOffset = _serializer.uint16(obj.m4, buffer, bufferOffset);
    // Serialize message field [ID]
    bufferOffset = _serializer.uint16(obj.ID, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MotorControlwID
    let len;
    let data = new MotorControlwID(null);
    // Deserialize message field [m1Motor]
    data.m1Motor = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [m2]
    data.m2 = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [m3]
    data.m3 = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [m4]
    data.m4 = _deserializer.uint16(buffer, bufferOffset);
    // Deserialize message field [ID]
    data.ID = _deserializer.uint16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 10;
  }

  static datatype() {
    // Returns string type for a message object
    return 'crazyflie_mpc/MotorControlwID';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '53816296b5bd669972d937c31e11fb61';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint16 m1Motor
    uint16 m2
    uint16 m3
    uint16 m4
    uint16 ID
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MotorControlwID(null);
    if (msg.m1Motor !== undefined) {
      resolved.m1Motor = msg.m1Motor;
    }
    else {
      resolved.m1Motor = 0
    }

    if (msg.m2 !== undefined) {
      resolved.m2 = msg.m2;
    }
    else {
      resolved.m2 = 0
    }

    if (msg.m3 !== undefined) {
      resolved.m3 = msg.m3;
    }
    else {
      resolved.m3 = 0
    }

    if (msg.m4 !== undefined) {
      resolved.m4 = msg.m4;
    }
    else {
      resolved.m4 = 0
    }

    if (msg.ID !== undefined) {
      resolved.ID = msg.ID;
    }
    else {
      resolved.ID = 0
    }

    return resolved;
    }
};

module.exports = MotorControlwID;
