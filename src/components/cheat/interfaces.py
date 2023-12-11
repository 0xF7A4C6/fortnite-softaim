from enum import IntEnum
from ctypes import (
    c_short,
    c_ulong,
    c_ushort,
    c_long,
    Structure,
    Union,
    POINTER,
)

PUL = POINTER(c_ulong)
EXTRA = c_ulong(0)


class MouseEvent(IntEnum):
    MOUSE_MOVE = 0x0001
    MOUSE_LEFT_DOWN = 0x0002
    MOUSE_LEFT_UP = 0x0004


class KeyBdInput(Structure):
    _fields_ = [
        ("wVk", c_ushort),
        ("wScan", c_ushort),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(Structure):
    _fields_ = [
        ("uMsg", c_ulong),
        ("wParamL", c_short),
        ("wParamH", c_ushort),
    ]


class MouseInput(Structure):
    _fields_ = [
        ("dx", c_long),
        ("dy", c_long),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


class Input(Structure):
    _fields_ = [
        ("type", c_ulong),
        ("ii", Input_I),
    ]


class POINT(Structure):
    _fields_ = [
        ("x", c_long),
        ("y", c_long),
    ]
