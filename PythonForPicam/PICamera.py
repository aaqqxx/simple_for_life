# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

from PiTypes import *
from PiTypesMore import *
from PiParameterLookup import *
from PiFunctions import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

"""

"""


def pointer(x):
    """Returns a ctypes pointer"""
    ptr = ctypes.pointer(x)
    return ptr


def load(x):
    """Loads DLL library where argument is location of library"""
    x = ctypes.cdll.LoadLibrary(x)
    return x


class PICamera_Params_STRUCT():
    def __init__(self):
        self.temperature_setpoint = piflt()
        self.exposure_time = piflt()
        self.readout_control_mode = PicamEnumeratedType()
        self.adc_quality = PicamEnumeratedType()
        # piflt adc_speed=
        self.adc_speed = PicamEnumeratedType()
        self.adc_analog_gain = PicamEnumeratedType()
        self.adc_em_gain = piint()
        self.trigger_response = PicamEnumeratedType()
        self.shutter_mode = PicamEnumeratedType()


class PICamera():
    def __init__(self):
        self.inited = pibln()
        self.camera = PicamHandle()
        self.id = PicamCameraID()
        self.serial_number = ctypes.c_char_p('Demo Cam 1')
        self.data = PicamAvailableData()
        self.errors = PicamAcquisitionErrorsMask()
        self.readoutstride = piint(0)
        pass

    def init(self):
        print "error =", Picam_IsLibraryInitialized(pointer(self.inited))
        if not self.inited:
            print "before Picam_InitializeLibrary()......"
            self.errors = Picam_InitializeLibrary()
            print "PicamError error =", self.errors

        # logging.error( Picam_OpenFirstCamera(pointer(self.camera)))
        # logging.error(PicamAcquisitionErrorsMask(0))


        if Picam_OpenFirstCamera(pointer(self.camera)) == "PicamError_None":
            Picam_GetCameraID(pointer(self.camera), pointer(self.id))
            print "Open First Camera successfully!"
            # print self.id.serial_number
        else:
            print 'Preparing to connect Demo Camera'
            model = ctypes.c_int(201)
            # serial_number = ctypes.c_char_p('Demo Cam 1')
            """
            PICAM_API Picam_ConnectDemoCamera(
            PicamModel     model,
            const pichar*  serial_number,
            PicamCameraID* id );
            """
            print 'Demo camera connetcted with return value = ', Picam_ConnectDemoCamera(model, self.serial_number,
                                                                                         pointer(self.id))
            print '\n'

            print 'Camera model is ', self.id.model
            print 'Camera computer interface is ', self.id.computer_interface
            print 'Camera sensor_name is ', self.id.sensor_name
            print 'Camera serial number is', self.id.serial_number
            print '\n'

        pass

    def acquire(self):
        readoutstride = piint(0)
        readout_count = pi64s(1)
        readout_time_out = piint(10000)
        available = PicamAvailableData()
        errors = PicamAcquisitionErrorsMask()

        Picam_GetParameterIntegerValue(self.camera, ctypes.c_int(PicamParameter_ReadoutStride),
                                       ctypes.byref(readoutstride))

        Picam_Acquire.argtypes = PicamHandle, pi64s, piint, ctypes.POINTER(PicamAvailableData), ctypes.POINTER(
            PicamAcquisitionErrorsMask)
        Picam_Acquire.restype = piint

        res = Picam_Acquire(self.camera, readout_count, readout_time_out, ctypes.byref(available),
                            ctypes.byref(errors))

        if res == "PicamError_None":
            # print available.initial_readout
            DataArrayPointerType = ctypes.POINTER(pi16u * 1048576)
            print "available.initial_readout: ", available.initial_readout
            tmp = ctypes.cast(available.initial_readout, DataArrayPointerType)
            print "tmp.contents", tmp.contents

            tmp1 = np.array(tmp.contents)
            tmp1 = tmp1.reshape(1024,1024)
            #tmp1.dtype=np.uint16
            print type(tmp1[0][0]),tmp1[0][0]
            print tmp1.shape,tmp1
            #tmp1=np.asarray(tmp1)
            #tmp1=np.arange(0,1024*1024,1).reshape(1024,1024)
            # im=Image.fromarray(tmp1)
            #im.show()
            # im.save("test.png")
            # data_array=[]
            # for each in tmp.contents:
            #    data_array.append(int(each))
            # data_array=

            print "Initial readout type is", type(available.initial_readout)
            return available
        else:
            print "Error: Camera only collected ", available.readout_count
            return None
        pass

    def acquire_to_save(self):
        available = self.acquire()

        if (available!=None):
            """ Test Routine to Access Data """

            """ Create an array type to hold 1024x1024 16bit integers """
            DataArrayType = pi16u * 1048576

            """ Create pointer type for the above array type """
            DataArrayPointerType = ctypes.POINTER(pi16u * 1048576)

            """ Create an instance of the pointer type, and point it to initial readout contents (memory address?) """
            DataPointer = ctypes.cast(available.initial_readout, DataArrayPointerType)

            """ Create a separate array with readout contents """
            data = DataPointer.contents

            """ Write contents of Data to binary file"""
            libc = ctypes.cdll.msvcrt
            fopen = libc.fopen
            fopen.argtypes = ctypes.c_char_p, ctypes.c_char_p
            fopen.restype = ctypes.c_void_p

            fwrite = libc.fwrite
            fwrite.argtypes = ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_void_p
            fwrite.restype = ctypes.c_size_t

            fclose = libc.fclose
            fclose.argtypes = ctypes.c_void_p,
            fclose.restype = ctypes.c_int

            fp = fopen('PythonBinOutput.raw', 'wb')
            readoutstride = piint(0)
            print "Getting readout stride. ", Picam_GetParameterIntegerValue(self.camera, ctypes.c_int(PicamParameter_ReadoutStride),
                                                                         ctypes.byref(readoutstride))
            print "readoutstride.value is",readoutstride.value
            print 'fwrite returns: ', fwrite(data, readoutstride.value, 1, fp)

            fclose(fp)
            pass

    def get_camera_model(self):
        string = ctypes.c_char_p("              ")
        Picam_GetEnumerationString(PicamEnumeratedType(2), self.id.model, ctypes.byref(string))
        res = string.value + self.id.serial_number + self.id.sensor_name
        print res
        return res
        # pass

    def set_temperature(self, temp):
        pass

    def read_temperature(self, temperature, status):
        pass

    def set_exposure_time(self, exposure_time):
        # error = PicamError()
        error = Picam_SetParameterFloatingPointValue(self.camera,PicamParameter_ExposureTime,exposure_time)
        print "error is ",error
        pass

    def set_readout_mode(self, readout_mode):
        pass

    def set_adc_quality(self, quality):
        pass

    def set_adc_speed(self, speed):
        pass

    def set_adc_analog_gain(self, analog_gain):
        pass

    def set_adc_em_gain(self, em_gain):
        pass

    def set_trigger_mode(self, trigger_mode):
        pass

    def set_shutter_mode(self, shutter_mode):
        pass

    def commit_common_parameters(self):
        pass

    def read_common_parameters(self):
        pass

    def open_shutter(self):
        pass

    def close_shutter(self):
        pass

    def commit_param(self):
        # error = PicamError()
        committed = pibln()
        error = Picam_AreParametersCommitted( self.camera,ctypes.byref(committed))
        print "Picam_AreParametersCommitted exec res is",error
        print "Picam_AreParametersCommitted val is",committed
        failed_parameters_count = piint()
        failed_parameters = Picamparameter()
        Picam_CommitParameters()
        pass

if __name__ == "__main__":
    p = PICamera()
    p.init()
    p.set_exposure_time(50)
    p.commit_param()
    p.get_camera_model()
    # p.acquire_to_save()