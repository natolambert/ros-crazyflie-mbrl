
"use strict";

let Stop = require('./Stop.js')
let Land = require('./Land.js')
let UploadTrajectory = require('./UploadTrajectory.js')
let UpdateParams = require('./UpdateParams.js')
let SetGroupMask = require('./SetGroupMask.js')
let GoTo = require('./GoTo.js')
let sendPacket = require('./sendPacket.js')
let StartTrajectory = require('./StartTrajectory.js')
let Takeoff = require('./Takeoff.js')
let AddCrazyflie = require('./AddCrazyflie.js')
let RemoveCrazyflie = require('./RemoveCrazyflie.js')

module.exports = {
  Stop: Stop,
  Land: Land,
  UploadTrajectory: UploadTrajectory,
  UpdateParams: UpdateParams,
  SetGroupMask: SetGroupMask,
  GoTo: GoTo,
  sendPacket: sendPacket,
  StartTrajectory: StartTrajectory,
  Takeoff: Takeoff,
  AddCrazyflie: AddCrazyflie,
  RemoveCrazyflie: RemoveCrazyflie,
};
