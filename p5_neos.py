# Neos websocket version of this, pipes the data in a big list. (Not super useful)

dllFile = r".\p5dll.dll"

from ctypes import * 
import time
import os
import asyncio
import asyncio
from websockets import serve

# Define the data type for P5BOOL
P5BOOL = c_uint

# Define the structures
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


def run_dict(data):
    def concat_add(string,val,b):
        if b:
            if val:
                return string + f"{'True':16}"
            else:
                return string + f"{'False':16}"    
        elif type(val) == int:
            return string + f"{val:16}"
        if type(val) == float:
            return string + f"{val:16f}"

    current = 0
    out = ""
    for x in data:
        a = type(data[x])
        boo = x in ["Visible","button"]

        if a == list:
            for i,y in enumerate(data[x]):
                b = type(y)
                if b == list:
                    for j,z in enumerate(y):
                        out = concat_add(out, z)
                        current+=16
                else:
                    out = concat_add(out, y)
                    current+=16
        else:
            out = concat_add(out, data[x])
            current+=16
    return out

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

# Define the return type and arguments for P5_GetCount
P5_GetCount = p5dll.P5_GetCount
P5_GetCount.argtypes = []
P5_GetCount.restype = c_int

# Define the return type and arguments for P5_GetStatePointer
P5StatePointer = POINTER(P5State)
P5_GetStatePointer = p5dll.P5_GetStatePointer
P5_GetStatePointer.argtypes = [c_int]
P5_GetStatePointer.restype = P5StatePointer

# Call the functions
result = P5_Init()
a = P5_GetCount()
print("Init Number:", result)
print("Number of gloves:", a)


async def echo(websocket):
    print("Got connection")
    #os.system("cls")
    #for x in result:
    #    print(f"{x:30}| ", result[x])

    async for message in websocket:
        print("Got message, sending data... ",end = "")
        data = P5_GetStatePointer(c_int(0))
        result = p5_state_to_dict(data.contents)
        await websocket.send(run_dict(result))
        print("Sent")

async def main():
    print("Running Server, waiting for connection...")
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())

P5_Close()