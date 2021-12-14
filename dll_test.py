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

def get_tag(tag,bytes, tag_bytes=None, tag_data_bytes=None):
    if tag_bytes is None and tag_data_bytes is None:
        tag_bytes = bytearray()
        tag_data_bytes = bytearray()
    tag_pos = re.search(tag,bytes).span()[0]
    len = bytes[tag_pos+2:tag_pos+4]
    t_start_pos = tag_pos
    td_start_pos = tag_pos+4
    stop_pos = tag_pos+int.from_bytes(len,byteorder='big')+2
    tag_bytes = tag_bytes+bytes[t_start_pos:stop_pos]
    tag_data_bytes = tag_data_bytes+bytes[td_start_pos:stop_pos]
    if bytes[stop_pos:stop_pos+2]==tag:
        tag_bytes, tag_data_bytes = get_tag(tag,bytes[stop_pos:], tag_bytes, tag_data_bytes)
    return tag_bytes, tag_data_bytes

def get_tag_data(bytes, data=None):
    if data is None:
        data = bytearray()
    tag = bytes[:2]
    

with open("input/air_original.JPG","rb") as file:
    file_content = bytearray(file.read())
# with open("1px.JPG","rb") as file:
#     template_file_content = bytearray(file.read())

tb_ffe1, tdb_ffe1 = get_tag(b"\xff\xe1",file_content)
tb_ffe2, tdb_ffe2 = get_tag(b"\xff\xe2",file_content)
tb_ffe3, tdb_ffe3 = get_tag(b"\xff\xe3",file_content)
tb_ffe4, tdb_ffe4 = get_tag(b"\xff\xe4",file_content)
tb_ffe5, tdb_ffe5 = get_tag(b"\xff\xe5",file_content)
prefix = bytearray(b"\xff\xd8")+tb_ffe1+tb_ffe2
suffix = tb_ffe4+tb_ffe5#+b"\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x03\x01\x22\x00\x02\x11\x01\x03\x11\x01"


file_size = len(prefix)+6+len(suffix)+1
res = (512,640)
temp_data_len = res[0]*res[1]
new_temp_data_len = 1
c_dirp_handle = c_void_p()
c_rjpeg_size = c_int32(file_size)
c_rjpeg_data = (c_uint8*file_size)()

tsdk = cdll.LoadLibrary("./libdirp.dll")
tsdk.dirp_register_app(b"DJI_TSDK")
c_verbose = c_int32(2)
tsdk.dirp_set_verbose_level(c_verbose)
c_temp_data_size = c_int32(2*new_temp_data_len)
c_temp_data = (c_float*new_temp_data_len)()
c_temp_data_pointer = cast(c_temp_data, POINTER(c_float))
temp_data = np.empty(temp_data_len, np.float)
c_measurement_params = c_measurement_params_struct()
c_measurement_params_pointer = pointer(c_measurement_params)
for i in range(temp_data_len):
    new_file_content = prefix+b'\xff\xe3\x00\x04'+tdb_ffe3[i*2:i*2+2]+suffix
    c_rjpeg_data = (c_uint8*file_size)(*new_file_content)
    c_rjpeg_data_pointer = cast(c_rjpeg_data, POINTER(c_uint8))
    ret = tsdk.dirp_create_from_rjpeg(c_rjpeg_data_pointer, c_rjpeg_size, byref(c_dirp_handle))

# set measurement parameters


    d=10.0
    h=77.0
    e=0.99
    r=23.0

    c_measurement_params.distance = d
    c_measurement_params.humidyty = h
    c_measurement_params.emissivity = e
    c_measurement_params.reflection = r
    tsdk.dirp_set_measurement_params(c_dirp_handle, c_measurement_params_pointer)
    tsdk.dirp_measure_ex(c_dirp_handle, c_temp_data_pointer, c_temp_data_size)
    temp_data[i] = c_temp_data_pointer[0]




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