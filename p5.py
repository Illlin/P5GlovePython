dllFile = r".\p5dll.dll"

from ctypes import *
import time
import os
import json

# Define the data type for P5BOOL
P5BOOL = c_uint

# Define the structures
class P5Data(Structure):
    _fields_ = [
        ("VendorID", c_char * 50),
        ("ProductID", c_char * 50),
        ("Version", c_char * 50),
        ("ProductString", c_char * 255),
        ("ManufacturerString", c_char * 255),
        ("SerialNumString", c_char * 255),
        ("m_nDeviceID", c_int),
        ("m_nMajorRevisionNumber", c_int),
        ("m_nMinorRevisionNumber", c_int),
        ("m_nGloveType", c_int),
        ("m_fx", c_float),
        ("m_fy", c_float),
        ("m_fz", c_float),
        ("m_fyaw", c_float),
        ("m_fpitch", c_float),
        ("m_froll", c_float),
        ("m_byBendSensor_Data", c_char * 5),
        ("m_byButtons", c_char * 4),
        ("m_fRotMat", c_float * 3 * 3),
    ]

class P5Info(Structure):
    _fields_ = [
        ("VendorID", c_char * 52),
        ("ProductID", c_char * 52),
        ("Version", c_char * 52),
        ("ProductString", c_char * 256),
        ("ManufacturerString", c_char * 256),
        ("SerialNumString", c_char * 256),
        ("DeviceID", c_int),
        ("MajorRevisionNumber", c_int),
        ("MinorRevisionNumber", c_int),
        ("GloveType", c_int),
        ("ActualLedPos", c_float * 3 * 10),
        ("LEDDistances", c_float * 10 * 10),
        ("Head1_VAngle", c_float),
        ("Head_HAngle", c_float),
        ("Head2_VAngle", c_float),
        ("Head2_HAngle", c_float),
        ("HeadSeparation", c_float),
        ("ACAdapterStatus", P5BOOL),
        ("FingerStraight", c_int * 5),
        ("FingerBent", c_int * 5),
        ("DeviceHandle", c_void_p),
        ("ThreadId", c_uint),
        ("ThreadHandle", c_uint),
        ("ThreadStatus", P5BOOL)
    ]

class P5State(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("RelativeX", c_float),
        ("RelativeY", c_float),
        ("RelativeZ", c_float),
        ("RelativeAvgX", c_float),
        ("RelativeAvgY", c_float),
        ("RelativeAvgZ", c_float),
        ("FilterPos", c_float * 3),
        ("Velocity", c_float * 3),
        ("Acceleration", c_float * 3),
        ("RotMat", c_float * 3 * 3),
        ("pitch", c_float),
        ("yaw", c_float),
        ("roll", c_float),
        ("FilterRotMat", c_float * 3 * 3),
        ("FilterPitch", c_float),
        ("FilterYaw", c_float),
        ("FilterRoll", c_float),
        ("AngularVelocity", c_float * 3),
        ("AngularAcceleration", c_float * 3),
        ("Visible", c_int),
        ("finger", c_ubyte * 5),
        ("FingerAbsolute", c_short * 5),
        ("FingerVelocity", c_float * 5),
        ("FingerAcceleration", c_float * 5),
        ("button", c_ubyte * 4),
        ("LedPos", c_float * 10 * 3),
        ("LedVelocity", c_float * 10 * 3),
        ("LedGeometricAccuracy", c_float * 10),
        ("LedVisible", c_ubyte * 10),
        ("TrackedLed", c_int),
        ("VisibleLedCount", c_int),
        ("VisibleLedNumber", c_char * 4),
        ("VisibleLedRaw", c_int * 4 * 3),
        ("VisibleLedV1Angle", c_float * 4),
        ("VisibleLedV2Angle", c_float * 4),
        ("VisibleLedHAngle", c_float * 4),
        ("VisibleLedPos", c_float * 4 * 3),
        ("TimeStamp", c_double),
        ("FrameRate", c_float),
        ("Frame", c_longlong),
    ]

def p5_state_to_dict(p5_state):
    p5_dict = {}
    p5_dict["x"] = p5_state.x
    p5_dict["y"] = p5_state.y
    p5_dict["z"] = p5_state.z
    p5_dict["RelativeX"] = p5_state.RelativeX
    p5_dict["RelativeY"] = p5_state.RelativeY
    p5_dict["RelativeZ"] = p5_state.RelativeZ
    p5_dict["RelativeAvgX"] = p5_state.RelativeAvgX
    p5_dict["RelativeAvgY"] = p5_state.RelativeAvgY
    p5_dict["RelativeAvgZ"] = p5_state.RelativeAvgZ
    p5_dict["FilterPos"] = [float(i) for i in p5_state.FilterPos]
    p5_dict["Velocity"] = [float(i) for i in p5_state.Velocity]
    p5_dict["Acceleration"] = [float(i) for i in p5_state.Acceleration]
    p5_dict["RotMat"] = [list(i) for i in p5_state.RotMat]
    p5_dict["pitch"] = p5_state.pitch
    p5_dict["yaw"] = p5_state.yaw
    p5_dict["roll"] = p5_state.roll
    p5_dict["FilterRotMat"] = [list(i) for i in p5_state.FilterRotMat]
    p5_dict["FilterPitch"] = p5_state.FilterPitch
    p5_dict["FilterYaw"] = p5_state.FilterYaw
    p5_dict["FilterRoll"] = p5_state.FilterRoll
    p5_dict["AngularVelocity"] = [float(i) for i in p5_state.AngularVelocity]
    p5_dict["AngularAcceleration"] = [float(i) for i in p5_state.AngularAcceleration]
    p5_dict["Visible"] = p5_state.Visible
    p5_dict["finger"] = [int(i) for i in p5_state.finger]
    p5_dict["FingerAbsolute"] = [int(i) for i in p5_state.FingerAbsolute]
    p5_dict["FingerVelocity"] = [float(i) for i in p5_state.FingerVelocity]
    p5_dict["FingerAcceleration"] = [float(i) for i in p5_state.FingerAcceleration]
    p5_dict["button"] = [int(i) for i in p5_state.button]
    p5_dict["LedPos"] = [list(i) for i in p5_state.LedPos]
    p5_dict["LedVelocity"] = [list(i) for i in p5_state.LedVelocity]
    p5_dict["LedGeometricAccuracy"] = [float(i) for i in p5_state.LedGeometricAccuracy]
    p5_dict["LedVisible"] = [int(i) for i in p5_state.LedVisible]
    p5_dict["TrackedLed"] = p5_state.TrackedLed
    p5_dict["VisibleLedCount"] = p5_state.VisibleLedCount
    p5_dict["VisibleLedNumber"] = [int(i) for i in p5_state.VisibleLedNumber]
    p5_dict["VisibleLedRaw"] = [list(i) for i in p5_state.VisibleLedRaw]
    p5_dict["VisibleLedV1Angle"] = [float(i) for i in p5_state.VisibleLedV1Angle]
    p5_dict["VisibleLedV2Angle"] = [float(i) for i in p5_state.VisibleLedV2Angle]
    p5_dict["VisibleLedHAngle"] = [float(i) for i in p5_state.VisibleLedHAngle]
    p5_dict["VisibleLedPos"] = [list(i) for i in p5_state.VisibleLedPos]
    p5_dict["TimeStamp"] = p5_state.TimeStamp
    p5_dict["FrameRate"] = p5_state.FrameRate
    p5_dict["Frame"] = p5_state.Frame
    return p5_dict


def p5_info_to_dict(p5_info):
    p5_dict = {}
    p5_dict['VendorID'] = p5_info.VendorID.decode('utf-8')
    p5_dict['ProductID'] = p5_info.ProductID.decode('utf-8')
    p5_dict['Version'] = p5_info.Version.decode('utf-8')
    p5_dict['ProductString'] = p5_info.ProductString.decode('utf-8')
    p5_dict['ManufacturerString'] = p5_info.ManufacturerString.decode('utf-8')
    p5_dict['SerialNumString'] = p5_info.SerialNumString.decode('utf-8')
    p5_dict['DeviceID'] = p5_info.DeviceID
    p5_dict['MajorRevisionNumber'] = p5_info.MajorRevisionNumber
    p5_dict['MinorRevisionNumber'] = p5_info.MinorRevisionNumber
    p5_dict['GloveType'] = p5_info.GloveType
    p5_dict['ActualLedPos'] = [list(i) for i in p5_info.ActualLedPos]
    p5_dict['LEDDistances'] = [list(i) for i in p5_info.LEDDistances]
    p5_dict['Head1_VAngle'] = p5_info.Head1_VAngle
    p5_dict['Head_HAngle'] = p5_info.Head_HAngle
    p5_dict['Head2_VAngle'] = p5_info.Head2_VAngle
    p5_dict['Head2_HAngle'] = p5_info.Head2_HAngle
    p5_dict['HeadSeparation'] = p5_info.HeadSeparation
    p5_dict['ACAdapterStatus'] = p5_info.ACAdapterStatus
    p5_dict['FingerStraight'] = list(p5_info.FingerStraight)
    p5_dict['FingerBent'] = list(p5_info.FingerBent)
    p5_dict['DeviceHandle'] = p5_info.DeviceHandle
    p5_dict['ThreadId'] = p5_info.ThreadId
    p5_dict['ThreadHandle'] = p5_info.ThreadHandle
    p5_dict['ThreadStatus'] = p5_info.ThreadStatus
    return p5_dict

# Load the DLL
p5dll = CDLL(dllFile)

# Define the function P5_Init
P5_Init = p5dll.P5_Init
P5_Init.argtypes = []
P5_Init.restype = P5BOOL

# Define the return type and arguments for P5_Close
P5_Close = p5dll.P5_Close
P5_Close.argtypes = []
P5_Close.restype = None

# Define the return type and arguments for P5_GetCP5DLL
P5_GetCP5DLL = p5dll.P5_GetCP5DLL
P5_GetCP5DLL.argtypes = []
P5_GetCP5DLL.restype = c_void_p

# Define the return type and arguments for P5_GetCP5
P5_GetCP5 = p5dll.P5_GetCP5
P5_GetCP5.argtypes = []
P5_GetCP5.restype = c_void_p

# Define the return type and arguments for P5_GetCount
P5_GetCount = p5dll.P5_GetCount
P5_GetCount.argtypes = []
P5_GetCount.restype = c_int

# Define the return type and arguments for P5_GetDataPointer
P5DataPointer = POINTER(P5Data)
P5_GetDataPointer = p5dll.P5_GetDataPointer
P5_GetDataPointer.argtypes = [c_int]
P5_GetDataPointer.restype = P5DataPointer

# Define the return type and arguments for P5_GetStatePointer
P5StatePointer = POINTER(P5State)
P5_GetStatePointer = p5dll.P5_GetStatePointer
P5_GetStatePointer.argtypes = [c_int]
P5_GetStatePointer.restype = P5StatePointer

# Define the return type and arguments for P5_GetInfoPointer
P5InfoPointer = POINTER(P5Info)
P5_GetInfoPointer = p5dll.P5_GetInfoPointer
P5_GetInfoPointer.argtypes = [c_int]
P5_GetInfoPointer.restype = P5InfoPointer

# Define the return type and arguments for P5_GetPrivatePointer
P5_GetPrivatePointer = p5dll.P5_GetPrivatePointer
P5_GetPrivatePointer.argtypes = [c_int]
P5_GetPrivatePointer.restype = c_void_p

# Call the functions
result = P5_Init()
a = P5_GetCount()
print("Init Number:", result)
print("Number of gloves:", a)

data = P5_GetStatePointer(c_int(0))
result = p5_state_to_dict(data.contents)
print(json.dumps(result))

while True:
    #data = P5_GetInfoPointer(c_int(0))
    data = P5_GetStatePointer(c_int(0))
    #result = p5_info_to_dict(data.contents)
    result = p5_state_to_dict(data.contents)

    os.system("cls")
    for x in result:
        print(f"{x:30}| ", result[x])
    #display_P5Info(garbage)
    time.sleep(0.1)


P5_Close()