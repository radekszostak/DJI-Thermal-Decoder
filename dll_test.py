import os
import struct
import numpy as np
import matplotlib.pyplot as plt

from ctypes import (
    c_float,
    c_uint8,
    cdll,
    c_int32,
    c_void_p,
    Structure,
    POINTER,
    cast,
    create_string_buffer,
    byref,
    pointer
)

from numpy.lib.function_base import _cov_dispatcher

with open("input/air_original.JPG","rb") as file:
    file_content = bytearray(file.read())
file_size = len(file_content)


c_dirp_handle = c_void_p()
c_rjpeg_size = c_int32(file_size)
c_rjpeg_data = (c_uint8*file_size)(*file_content)
c_rjpeg_data_pointer = cast(c_rjpeg_data, POINTER(c_uint8))
tsdk = cdll.LoadLibrary("C:/Radek/Doktorat/Badania/raw_thermo/DJIThermalSDK/converter/libdirp.dll")
tsdk.dirp_register_app(b"DJI_TSDK")
ret = tsdk.dirp_create_from_rjpeg(c_rjpeg_data_pointer, c_rjpeg_size, byref(c_dirp_handle))

d = 10.0
h = 77.0
e = 0.99
r = 23.0
class c_measurement_params_struct(Structure):
    _fields_ = [("distance", c_float),
                ("humidyty", c_float),
                ("emissivity", c_float),
                ("reflection", c_float)]
c_measurement_params = c_measurement_params_struct(d,h,e,r)
c_measurement_params_pointer = pointer(c_measurement_params)
tsdk.dirp_set_measurement_params(c_dirp_handle, c_measurement_params_pointer)

res = (512,640)
temp_data_len = res[0]*res[1]
c_temp_data_size = c_int32(temp_data_len*4)
c_temp_data = (c_float*temp_data_len)()
c_temp_data_pointer = cast(c_temp_data, POINTER(c_float))
tsdk.dirp_measure_ex(c_dirp_handle, c_temp_data_pointer, c_temp_data_size)
temp_data = np.reshape(np.array(c_temp_data_pointer[:temp_data_len]),res)
plt.imshow(temp_data, cmap="viridis")
plt.show()
print("end")