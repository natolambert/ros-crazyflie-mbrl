# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from crazyflie_mpc/MotorControlwID.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class MotorControlwID(genpy.Message):
  _md5sum = "53816296b5bd669972d937c31e11fb61"
  _type = "crazyflie_mpc/MotorControlwID"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """uint16 m1Motor
uint16 m2
uint16 m3
uint16 m4
uint16 ID
"""
  __slots__ = ['m1Motor','m2','m3','m4','ID']
  _slot_types = ['uint16','uint16','uint16','uint16','uint16']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       m1Motor,m2,m3,m4,ID

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(MotorControlwID, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.m1Motor is None:
        self.m1Motor = 0
      if self.m2 is None:
        self.m2 = 0
      if self.m3 is None:
        self.m3 = 0
      if self.m4 is None:
        self.m4 = 0
      if self.ID is None:
        self.ID = 0
    else:
      self.m1Motor = 0
      self.m2 = 0
      self.m3 = 0
      self.m4 = 0
      self.ID = 0

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_5H().pack(_x.m1Motor, _x.m2, _x.m3, _x.m4, _x.ID))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      end = 0
      _x = self
      start = end
      end += 10
      (_x.m1Motor, _x.m2, _x.m3, _x.m4, _x.ID,) = _get_struct_5H().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_5H().pack(_x.m1Motor, _x.m2, _x.m3, _x.m4, _x.ID))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      end = 0
      _x = self
      start = end
      end += 10
      (_x.m1Motor, _x.m2, _x.m3, _x.m4, _x.ID,) = _get_struct_5H().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_5H = None
def _get_struct_5H():
    global _struct_5H
    if _struct_5H is None:
        _struct_5H = struct.Struct("<5H")
    return _struct_5H
