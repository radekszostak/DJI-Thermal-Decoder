import os
import struct
import re
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from ctypes import (
    c_float,
    c_uint8,
    cdll,
    c_int32,
    c_void_p,
    Structure,
    POINTER,
    cast,
    byref,
    pointer
)
class c_measurement_params_struct(Structure):
    _fields_ = [("distance", c_float),
                ("humidyty", c_float),
                ("emissivity", c_float),
                ("reflection", c_float)]
res = (512,640)


with open("input/air_original.JPG","rb") as file:
    file_content = bytearray(file.read())
e_precission = 0.01
e_start = 0.85
e_stop = 1
r_precission = 1
r_start = 20
r_stop = 30
e_list = np.arange(e_start,e_stop,e_precission)
r_list = np.arange(r_start,r_stop,r_precission)
e_array = np.full(res,0.99)
r_array = np.full(res,23.0)


file_size = len(file_content)

temp_data_len = res[0]*res[1]
c_dirp_handle = c_void_p()
c_rjpeg_size = c_int32(file_size)
c_rjpeg_data = (c_uint8*file_size)()

tsdk = cdll.LoadLibrary("./libdirp.dll")
tsdk.dirp_register_app(b"DJI_TSDK")
c_verbose = c_int32(0)
tsdk.dirp_set_verbose_level(c_verbose)
c_temp_data_size = c_int32(4*temp_data_len)
c_temp_data = (c_float*temp_data_len)()
c_temp_data_pointer = cast(c_temp_data, POINTER(c_float))
temp_data = np.empty(temp_data_len, np.float)
c_measurement_params = c_measurement_params_struct()
c_measurement_params_pointer = pointer(c_measurement_params)

c_rjpeg_data = (c_uint8*file_size)(*file_content)
c_rjpeg_data_pointer = cast(c_rjpeg_data, POINTER(c_uint8))
ret = tsdk.dirp_create_from_rjpeg(c_rjpeg_data_pointer, c_rjpeg_size, byref(c_dirp_handle))

# set measurement parameters


d=10.0
h=77.0
c_measurement_params.distance = d
c_measurement_params.humidyty = h
all_temp_data = []
for i in range(len(e_list)):
    row = []
    for j in range(len(r_list)):
        row.append(None)
    all_temp_data.append(row)

for e_i, e in enumerate(tqdm(e_list)):
    for r_i, r in enumerate(r_list):
        c_measurement_params.emissivity = e
        c_measurement_params.reflection = r
        
        tsdk.dirp_set_measurement_params(c_dirp_handle, c_measurement_params_pointer)
        tsdk.dirp_measure_ex(c_dirp_handle, c_temp_data_pointer, c_temp_data_size)
        all_temp_data[e_i][r_i] = np.reshape(np.array(c_temp_data_pointer[:temp_data_len]),res)
temp_data = np.zeros(res,np.float)
for i in tqdm(range(res[0])):
    for j in range(res[1]):
        e_i = round((e_array[i][j]-e_start)/e_precission)
        r_i = round((r_array[i][j]-r_start)/r_precission)
        temp_data[i][j] = all_temp_data[e_i][r_i][i][j]



plt.imshow(temp_data, cmap="viridis")
plt.show()

# # get original raw
# res = (512,640)
# raw_data_len = res[0]*res[1]
# c_raw_data_size = c_int32(raw_data_len*2)
# c_raw_data = (c_uint16*raw_data_len)()
# c_raw_data_pointer = cast(c_raw_data, POINTER(c_uint16))
# tsdk.dirp_get_original_raw(c_dirp_handle,c_raw_data_pointer,c_raw_data_size)
# raw_data = np.array(c_raw_data_pointer[:raw_data_len], dtype=np.ushort).tobytes()
# with open("raw.raw","wb") as file:
#     file.write(raw_data)
# #plt.imshow(raw_data, cmap="viridis")
# #plt.show()
print("end")