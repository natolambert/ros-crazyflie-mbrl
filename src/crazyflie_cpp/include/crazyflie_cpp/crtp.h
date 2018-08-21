#pragma once

#include "Crazyradio.h"
#include <cstdint>

static int const CRTP_MAX_DATA_SIZE = 30;
static int const CRTP_MAXSIZE = 31;
#define CHECKSIZE(s) static_assert(sizeof(s) <= CRTP_MAXSIZE, #s " packet is too large");

static int const CRTP_MAXSIZE_RESPONSE = 32;
#define CHECKSIZE_RESPONSE(s) static_assert(sizeof(s) <= CRTP_MAXSIZE_RESPONSE, #s " packet is too large");

// Header
struct crtp
{
  constexpr crtp(uint8_t port, uint8_t channel)
    : channel(channel)
    , link(3)
    , port(port)
  {
  }

  crtp(uint8_t byte)
  {
    channel = (byte >> 0) & 0x3;
    link    = (byte >> 2) & 0x3;
    port    = (byte >> 4) & 0xF;
  }

  bool operator==(const crtp& other) const {
    return channel == other.channel && port == other.port;
  }

  uint8_t channel:2;
  uint8_t link:2;
  uint8_t port:4;
} __attribute__((packed));

// Packet structure definition
typedef struct {
  uint8_t size;
  union {
    struct {
      uint8_t header;
      uint8_t data[CRTP_MAX_DATA_SIZE];
    };
    uint8_t raw[CRTP_MAX_DATA_SIZE+1];
  };
} crtpPacket_t;

// Port 0 (Console)
struct crtpConsoleResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return crtp(response.data[0]) == crtp(0, 0);
    }

    crtp header;
    char text[31];
};
CHECKSIZE_RESPONSE(crtpConsoleResponse)

// Port 2 (Parameters)

struct crtpParamTocGetItemResponse;
struct crtpParamTocGetItemRequest
{
  crtpParamTocGetItemRequest(
    uint8_t id)
    : header(2, 0)
    , command(0)
    , id(id)
  {
  }

  bool operator==(const crtpParamTocGetItemRequest& other) const {
    return header == other.header && command == other.command && id == other.id;
  }

  typedef crtpParamTocGetItemResponse Response;

  const crtp header;
  const uint8_t command;
  uint8_t id;
} __attribute__((packed));
CHECKSIZE(crtpParamTocGetItemRequest)

struct crtpParamTocGetItemResponse
{
  static bool match(const Crazyradio::Ack& response) {
    return response.size > 5 &&
           crtp(response.data[0]) == crtp(2, 0) &&
           response.data[1] == 0;
  }

  crtpParamTocGetItemRequest request;
  uint8_t length:2; // one of ParamLength
  uint8_t type:1;   // one of ParamType
  uint8_t sign:1;   // one of ParamSign
  uint8_t res0:2;   // reserved
  uint8_t readonly:1;
  uint8_t group:1;  // one of ParamGroup
  char text[28]; // group, name
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpParamTocGetItemResponse)

struct crtpParamTocGetInfoResponse;
struct crtpParamTocGetInfoRequest
{
  crtpParamTocGetInfoRequest()
    : header(2, 0)
    , command(1)
  {
  }

  bool operator==(const crtpParamTocGetInfoRequest& other) const {
    return header == other.header && command == other.command;
  }

  typedef crtpParamTocGetInfoResponse Response;

  const crtp header;
  const uint8_t command;
} __attribute__((packed));
CHECKSIZE(crtpParamTocGetInfoRequest)

struct crtpParamTocGetInfoResponse
{
  static bool match(const Crazyradio::Ack& response) {
    return response.size == 7 &&
           crtp(response.data[0]) == crtp(2, 0) &&
           response.data[1] == 1;
  }

  crtpParamTocGetInfoRequest request;
  uint8_t numParam;
  uint32_t crc;
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpParamTocGetInfoResponse)

struct crtpParamValueResponse;
struct crtpParamReadRequest
{
  crtpParamReadRequest(
    uint8_t id)
    : header(2, 1)
    , id(id)
  {
  }

  bool operator==(const crtpParamReadRequest& other) const {
    return header == other.header && id == other.id;
  }

  typedef crtpParamValueResponse Response;

  const crtp header;
  const uint8_t id;
} __attribute__((packed));
CHECKSIZE(crtpParamReadRequest)

template <class T>
struct crtpParamWriteRequest
{
  crtpParamWriteRequest(
    uint8_t id,
    const T& value)
    : header(2, 2)
    , id(id)
    , value(value)
    {
    }

    const crtp header;
    const uint8_t id;
    const T value;
} __attribute__((packed));
CHECKSIZE(crtpParamWriteRequest<double>) // largest kind of param

struct crtpParamValueResponse
{
  static bool match(const Crazyradio::Ack& response) {
    return response.size > 2 &&
           (crtp(response.data[0]) == crtp(2, 1) ||
            crtp(response.data[0]) == crtp(2, 2));
  }

  crtpParamReadRequest request;
  union {
    uint8_t valueUint8;
    int8_t valueInt8;
    uint16_t valueUint16;
    int16_t valueInt16;
    uint32_t valueUint32;
    int32_t valueInt32;
    float valueFloat;
  };
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpParamValueResponse)

// Port 3 (Commander)

struct crtpSetpointRequest
{
  crtpSetpointRequest(
    float roll,
    float pitch,
    float yawrate,
    uint16_t thrust)
    : header(0x03, 0)
    , roll(roll)
    , pitch(pitch)
    , yawrate(yawrate)
    , thrust(thrust)
  {
  }
  const crtp header;
  float roll;
  float pitch;
  float yawrate;
  uint16_t thrust;
}  __attribute__((packed));
CHECKSIZE(crtpSetpointRequest)

// Port 3 (commander)
struct crtpCompactSetpointRequest
{
  crtpCompactSetpointRequest(
    uint32_t packed)
    : header(0x03, 0)
    , packed(packed)
  {
  }
  const crtp header;
  uint32_t packed;
}  __attribute__((packed));
CHECKSIZE(crtpSetpointRequest)

// Lambert added with packet ID Port 3 (commander)
struct crtpCompactSetpointRequestwID
{
  crtpCompactSetpointRequestwID(
    uint32_t packed,
    uint16_t packet_ID)
    : header(0x03, 0)
    , packed(packed)
    , packet_ID(packet_ID)
  {
  }
  const crtp header;
  uint32_t packed;
  uint16_t packet_ID;
}  __attribute__((packed));
CHECKSIZE(crtpSetpointRequest)

// Port 4 (Memory access)

struct crtpMemoryGetNumberRequest
{
  crtpMemoryGetNumberRequest()
    : header(0x04, 0)
    , command(1)
  {
  }
  const crtp header;
  const uint8_t command;
}  __attribute__((packed));
CHECKSIZE(crtpMemoryGetNumberRequest)

struct crtpMemoryGetNumberResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size == 3 &&
             crtp(response.data[0]) == crtp(4, 0) &&
             response.data[1] == 1;
    }

    crtpMemoryGetNumberRequest request;
    uint8_t numberOfMemories;
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpMemoryGetNumberResponse)

struct crtpMemoryGetInfoRequest
{
  crtpMemoryGetInfoRequest(
    uint8_t memId)
    : header(0x04, 0)
    , command(2)
    , memId(memId)
  {
  }
  const crtp header;
  const uint8_t command;
  uint8_t memId;
}  __attribute__((packed));
CHECKSIZE(crtpMemoryGetInfoRequest)

enum crtpMemoryType : uint8_t
{
  EEPROM = 0x00,
  OW     = 0x01,
  LED12  = 0x10,
  LOCO   = 0x11,
};

struct crtpMemoryGetInfoResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size > 2 &&
             crtp(response.data[0]) == crtp(4, 0) &&
             response.data[1] == 2;
    }

    crtpMemoryGetInfoRequest request;
    crtpMemoryType memType;
    uint32_t memSize; // Bytes
    uint64_t memAddr; // valid for OW and EEPROM
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpMemoryGetInfoResponse)

struct crtpMemoryReadRequest
{
  crtpMemoryReadRequest(
    uint8_t memId,
    uint32_t memAddr,
    uint8_t length)
    : header(0x04, 1)
    , memId(memId)
    , memAddr(memAddr)
    , length(length)
  {
  }
  const crtp header;
  uint8_t memId;
  uint32_t memAddr;
  uint8_t length;
}  __attribute__((packed));
CHECKSIZE(crtpMemoryReadRequest)

struct crtpMemoryReadResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size > 2 &&
             crtp(response.data[0]) == crtp(4, 1);
    }

    crtp header;
    uint8_t memId;
    uint32_t memAddr;
    uint8_t status;
    uint8_t data[24];
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpMemoryReadResponse)

struct crtpMemoryWriteRequest
{
  crtpMemoryWriteRequest(
    uint8_t memId,
    uint32_t memAddr)
    : header(0x04, 2)
    , memId(memId)
    , memAddr(memAddr)
  {
  }
  const crtp header;
  uint8_t memId;
  uint32_t memAddr;
  uint8_t data[24];
}  __attribute__((packed));
CHECKSIZE(crtpMemoryWriteRequest)

struct crtpMemoryWriteResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size > 2 &&
             crtp(response.data[0]) == crtp(4, 2);
    }

    crtp header;
    uint8_t memId;
    uint32_t memAddr;
    uint8_t status;
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpMemoryWriteResponse)

// Port 5 (Data logging)

struct crtpLogGetInfoResponse;
struct crtpLogGetInfoRequest
{
  crtpLogGetInfoRequest()
    : header(5, 0)
    , command(1)
    {
    }

  bool operator==(const crtpLogGetInfoRequest& other) const {
    return header == other.header && command == other.command;
  }

  typedef crtpLogGetInfoResponse Response;

  const crtp header;
  const uint8_t command;
} __attribute__((packed));
CHECKSIZE(crtpLogGetInfoRequest)

struct crtpLogGetInfoResponse
{
  static bool match(const Crazyradio::Ack& response) {
    return response.size == 9 &&
           crtp(response.data[0]) == crtp(5, 0) &&
           response.data[1] == 1;
  }

  crtpLogGetInfoRequest request;
  // Number of log items contained in the log table of content
  uint8_t log_len;
  // CRC values of the log TOC memory content. This is a fingerprint of the copter build that can be used to cache the TOC
  uint32_t log_crc;
  // Maximum number of log packets that can be programmed in the copter
  uint8_t log_max_packet;
  // Maximum number of operation programmable in the copter. An operation is one log variable retrieval programming
  uint8_t log_max_ops;
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpLogGetInfoResponse)

struct crtpLogGetItemResponse;
struct crtpLogGetItemRequest
{
  crtpLogGetItemRequest(uint8_t id)
    : header(5, 0)
    , command(0)
    , id(id)
  {
  }

  bool operator==(const crtpLogGetItemRequest& other) const {
    return header == other.header && command == other.command && id == other.id;
  }

  typedef crtpLogGetItemResponse Response;

  const crtp header;
  const uint8_t command;
  uint8_t id;
} __attribute__((packed));
CHECKSIZE(crtpLogGetItemRequest)

struct crtpLogGetItemResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size > 5 &&
             crtp(response.data[0]) == crtp(5, 0) &&
             response.data[1] == 0;
    }

    crtpLogGetItemRequest request;
    uint8_t type;
    char text[28]; // group, name
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpLogGetItemResponse)

struct logBlockItem {
  uint8_t logType;
  uint8_t id;
} __attribute__((packed));

struct crtpLogCreateBlockRequest
{
  crtpLogCreateBlockRequest()
  : header(5, 1)
  , command(0)
  {
  }

  const crtp header;
  const uint8_t command;
  uint8_t id;
  logBlockItem items[14];
} __attribute__((packed));
CHECKSIZE(crtpLogCreateBlockRequest)

// struct logAppendBlockRequest
// {
//   logAppendBlockRequest()
//     : header(5, 1)
//     , command(1)
//     {
//     }

//     const crtp header;
//     const uint8_t command;
//     uint8_t id;
//     logBlockItem items[16];
// } __attribute__((packed));

// struct logDeleteBlockRequest
// {
//   logDeleteBlockRequest()
//     : header(5, 1)
//     , command(2)
//     {
//     }

//     const crtp header;
//     const uint8_t command;
//     uint8_t id;
// } __attribute__((packed));

struct crtpLogStartRequest
{
  crtpLogStartRequest(
    uint8_t id,
    uint8_t period)
    : header(5, 1)
    , command(3)
    , id(id)
    , period(period)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t id;
    uint8_t period; // in increments of 10ms
} __attribute__((packed));
CHECKSIZE(crtpLogStartRequest)

struct crtpLogStopRequest
{
  crtpLogStopRequest(
    uint8_t id)
    : header(5, 1)
    , command(4)
    , id(id)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t id;
} __attribute__((packed));
CHECKSIZE(crtpLogStopRequest)

struct crtpLogResetRequest
{
  crtpLogResetRequest()
    : header(5, 1)
    , command(5)
    {
    }

    const crtp header;
    const uint8_t command;
} __attribute__((packed));
CHECKSIZE(crtpLogResetRequest)

enum crtpLogControlResult {
  crtpLogControlResultOk            = 0,
  crtpLogControlResultOutOfMemory   = 12, // ENOMEM
  crtpLogControlResultCmdNotFound   = 8,  // ENOEXEC
  crtpLogControlResultWrongBlockId  = 2,  // ENOENT
  crtpLogControlResultBlockTooLarge = 7,  // E2BIG
  crtpLogControlResultBlockExists   = 17, // EEXIST

};

struct crtpLogControlResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size == 4 &&
             crtp(response.data[0]) == crtp(5, 1);
    }

    crtp header;
    uint8_t command;
    uint8_t requestByte1;
    uint8_t result; // one of crtpLogControlResult
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpLogControlResponse)

struct crtpLogDataResponse
{
    static bool match(const Crazyradio::Ack& response) {
      return response.size > 4 &&
             crtp(response.data[0]) == crtp(5, 2);
    }

    crtp header;
    uint8_t blockId;
    uint8_t timestampLo;
    uint16_t timestampHi;
    uint8_t data[26];
} __attribute__((packed));
CHECKSIZE_RESPONSE(crtpLogDataResponse)

// Port 0x06 (External Position Update)

struct crtpExternalPositionUpdate
{
  crtpExternalPositionUpdate(
    float x,
    float y,
    float z)
    : header(0x06, 0)
    , x(x)
    , y(y)
    , z(z)
  {
  }
  const crtp header;
  float x;
  float y;
  float z;
}  __attribute__((packed));
CHECKSIZE(crtpExternalPositionUpdate)

struct crtpExternalPositionPacked
{
  crtpExternalPositionPacked()
    : header(0x06, 2)
  {
  }
  const crtp header;
  struct {
    uint8_t id;
    int16_t x; // mm
    int16_t y; // mm
    int16_t z; // mm
  } __attribute__((packed)) positions[4];
}  __attribute__((packed));
CHECKSIZE(crtpExternalPositionPacked)

struct crtpStopRequest
{
  crtpStopRequest();
  const crtp header;
  uint8_t type;
} __attribute__((packed));
CHECKSIZE(crtpStopRequest)

struct crtpHoverSetpointRequest
{
  crtpHoverSetpointRequest(
    float vx,
    float vy,
    float yawrate,
    float zDistance);
  const crtp header;
  uint8_t type;
  float vx;
  float vy;
  float yawrate;
  float zDistance;
} __attribute__((packed));
CHECKSIZE(crtpHoverSetpointRequest)

struct crtpPositionSetpointRequest
{
  crtpPositionSetpointRequest(
    float x,
    float y,
    float z,
    float yaw);
  const crtp header;
  uint8_t type;
  float x;
  float y;
  float z;
  float yaw;
} __attribute__((packed));
CHECKSIZE(crtpPositionSetpointRequest)

// Port 0x07 (Generic Setpoint)

struct crtpFullStateSetpointRequest
{
  crtpFullStateSetpointRequest(
    float x, float y, float z,
    float vx, float vy, float vz,
    float ax, float ay, float az,
    float qx, float qy, float qz, float qw,
    float rollRate, float pitchRate, float yawRate);
  const crtp header;
  uint8_t type;
  int16_t x;
  int16_t y;
  int16_t z;
  int16_t vx;
  int16_t vy;
  int16_t vz;
  int16_t ax;
  int16_t ay;
  int16_t az;
  int32_t quat; // compressed quaternion, xyzw
  int16_t omegax;
  int16_t omegay;
  int16_t omegaz;
} __attribute__((packed));
CHECKSIZE(crtpFullStateSetpointRequest)

// Port 0x08 (High-level Setpoints)

struct crtpCommanderHighLevelSetGroupMaskRequest
{
  crtpCommanderHighLevelSetGroupMaskRequest(
    uint8_t groupMask)
    : header(0x08, 0)
    , command(0)
    , groupMask(groupMask)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask;
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelSetGroupMaskRequest)

struct crtpCommanderHighLevelTakeoffRequest
{
  crtpCommanderHighLevelTakeoffRequest(
    uint8_t groupMask,
    float height,
    float duration)
    : header(0x08, 0)
    , command(1)
    , groupMask(groupMask)
    , height(height)
    , duration(duration)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask;        // mask for which CFs this should apply to
    float height;             // m (absolute)
    float duration;           // s (time it should take until target height is reached)
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelTakeoffRequest)

struct crtpCommanderHighLevelLandRequest
{
  crtpCommanderHighLevelLandRequest(
    uint8_t groupMask,
    float height,
    float duration)
    : header(0x08, 0)
    , command(2)
    , groupMask(groupMask)
    , height(height)
    , duration(duration)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask;        // mask for which CFs this should apply to
    float height;             // m (absolute)
    float duration;           // s (time it should take until target height is reached)
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelLandRequest)

struct crtpCommanderHighLevelStopRequest
{
  crtpCommanderHighLevelStopRequest(
    uint8_t groupMask)
    : header(0x08, 0)
    , command(3)
    , groupMask(groupMask)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask;        // mask for which CFs this should apply to
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelStopRequest)

struct crtpCommanderHighLevelGoToRequest
{
  crtpCommanderHighLevelGoToRequest(
    uint8_t groupMask,
    bool relative,
    float x,
    float y,
    float z,
    float yaw,
    float duration)
    : header(0x08, 0)
    , command(4)
    , groupMask(groupMask)
    , relative(relative)
    , x(x)
    , y(y)
    , z(z)
    , yaw(yaw)
    , duration(duration)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask; // mask for which CFs this should apply to
    uint8_t relative;  // set to true, if position/yaw are relative to current setpoint
    float x; // m
    float y; // m
    float z; // m
    float yaw; // deg
    float duration; // sec
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelGoToRequest)

struct crtpCommanderHighLevelStartTrajectoryRequest
{
  crtpCommanderHighLevelStartTrajectoryRequest(
    uint8_t groupMask,
    bool relative,
    bool reversed,
    uint8_t trajectoryId,
    float timescale)
    : header(0x08, 0)
    , command(5)
    , groupMask(groupMask)
    , relative(relative)
    , reversed(reversed)
    , trajectoryId(trajectoryId)
    , timescale(timescale)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t groupMask; // mask for which CFs this should apply to
    uint8_t relative;  // set to true, if trajectory should be shifted to current setpoint
    uint8_t reversed;  // set to true, if trajectory should be executed in reverse
    uint8_t trajectoryId; // id of the trajectory (previously defined by COMMAND_DEFINE_TRAJECTORY)
    float timescale; // time factor; 1 = original speed; >1: slower; <1: faster
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelStartTrajectoryRequest)

enum TrajectoryLocation_e {
  TRAJECTORY_LOCATION_INVALID = 0,
  TRAJECTORY_LOCATION_MEM     = 1, // for trajectories that are uploaded dynamically
  // Future features might include trajectories on flash or uSD card
};

enum TrajectoryType_e {
  TRAJECTORY_TYPE_POLY4D = 0, // struct poly4d, see pptraj.h
  // Future types might include versions without yaw
};

struct trajectoryDescription
{
  uint8_t trajectoryLocation; // one of TrajectoryLocation_e
  uint8_t trajectoryType;     // one of TrajectoryType_e
  union
  {
    struct {
      uint32_t offset;  // offset in uploaded memory
      uint8_t n_pieces;
    } __attribute__((packed)) mem; // if trajectoryLocation is TRAJECTORY_LOCATION_MEM
  } trajectoryIdentifier;
} __attribute__((packed));

struct crtpCommanderHighLevelDefineTrajectoryRequest
{
  crtpCommanderHighLevelDefineTrajectoryRequest(
    uint8_t trajectoryId)
    : header(0x08, 0)
    , command(6)
    , trajectoryId(trajectoryId)
    {
    }

    const crtp header;
    const uint8_t command;
    uint8_t trajectoryId;
    struct trajectoryDescription description;
} __attribute__((packed));
CHECKSIZE(crtpCommanderHighLevelDefineTrajectoryRequest)

// Port 11 CrazySwarm Experimental

typedef uint16_t fp16_t;
typedef int16_t posFixed16_t;
typedef struct posFixed24_t
{
  uint8_t low;
  uint8_t middle;
  uint8_t high;
} posFixed24_t;

struct data_mocap {
  struct {
    uint8_t id;
    posFixed24_t x; // m
    posFixed24_t y; // m
    posFixed24_t z; // m
    uint32_t quat; // compressed quat, see quatcompress.h
  } __attribute__((packed)) pose[2];
} __attribute__((packed));

struct crtpPosExtBringup
{
  crtpPosExtBringup()
    : header(11, 1)
    {
      data.pose[0].id = 0;
      data.pose[1].id = 0;
    }

    const crtp header;
    struct data_mocap data;
} __attribute__((packed));
CHECKSIZE(crtpPosExtBringup)

// Port 13 (Platform)

// The crazyflie-nrf firmware sends empty packets with the signal strength, if nothing else is in the queue
struct crtpPlatformRSSIAck
{
    static bool match(const Crazyradio::Ack& response) {
      return crtp(response.data[0]) == crtp(15, 3);
    }

    crtp header;
    uint8_t reserved;
    uint8_t rssi;
};
CHECKSIZE_RESPONSE(crtpPlatformRSSIAck)
