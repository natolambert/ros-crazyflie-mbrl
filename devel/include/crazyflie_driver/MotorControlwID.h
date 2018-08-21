// Generated by gencpp from file crazyflie_driver/MotorControlwID.msg
// DO NOT EDIT!


#ifndef CRAZYFLIE_DRIVER_MESSAGE_MOTORCONTROLWID_H
#define CRAZYFLIE_DRIVER_MESSAGE_MOTORCONTROLWID_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace crazyflie_driver
{
template <class ContainerAllocator>
struct MotorControlwID_
{
  typedef MotorControlwID_<ContainerAllocator> Type;

  MotorControlwID_()
    : m1(0)
    , m2(0)
    , m3(0)
    , m4(0)
    , ID(0)  {
    }
  MotorControlwID_(const ContainerAllocator& _alloc)
    : m1(0)
    , m2(0)
    , m3(0)
    , m4(0)
    , ID(0)  {
  (void)_alloc;
    }



   typedef uint16_t _m1_type;
  _m1_type m1;

   typedef uint16_t _m2_type;
  _m2_type m2;

   typedef uint16_t _m3_type;
  _m3_type m3;

   typedef uint16_t _m4_type;
  _m4_type m4;

   typedef uint16_t _ID_type;
  _ID_type ID;





  typedef boost::shared_ptr< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> const> ConstPtr;

}; // struct MotorControlwID_

typedef ::crazyflie_driver::MotorControlwID_<std::allocator<void> > MotorControlwID;

typedef boost::shared_ptr< ::crazyflie_driver::MotorControlwID > MotorControlwIDPtr;
typedef boost::shared_ptr< ::crazyflie_driver::MotorControlwID const> MotorControlwIDConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::crazyflie_driver::MotorControlwID_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace crazyflie_driver

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'crazyflie_driver': ['/home/hiro/crazyflie_ros/src/crazyflie_driver/msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
{
  static const char* value()
  {
    return "df11cfbc0178ba6af8c99c3ea9325b85";
  }

  static const char* value(const ::crazyflie_driver::MotorControlwID_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xdf11cfbc0178ba6aULL;
  static const uint64_t static_value2 = 0xf8c99c3ea9325b85ULL;
};

template<class ContainerAllocator>
struct DataType< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
{
  static const char* value()
  {
    return "crazyflie_driver/MotorControlwID";
  }

  static const char* value(const ::crazyflie_driver::MotorControlwID_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint16 m1\n\
uint16 m2\n\
uint16 m3\n\
uint16 m4\n\
uint16 ID\n\
";
  }

  static const char* value(const ::crazyflie_driver::MotorControlwID_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.m1);
      stream.next(m.m2);
      stream.next(m.m3);
      stream.next(m.m4);
      stream.next(m.ID);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MotorControlwID_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::crazyflie_driver::MotorControlwID_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::crazyflie_driver::MotorControlwID_<ContainerAllocator>& v)
  {
    s << indent << "m1: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.m1);
    s << indent << "m2: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.m2);
    s << indent << "m3: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.m3);
    s << indent << "m4: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.m4);
    s << indent << "ID: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.ID);
  }
};

} // namespace message_operations
} // namespace ros

#endif // CRAZYFLIE_DRIVER_MESSAGE_MOTORCONTROLWID_H
