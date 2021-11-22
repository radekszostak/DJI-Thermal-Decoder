import numpy as np
d_arr = np.arange(1.0,25.0,1.0)
h_arr = np.arange(20.0,100.0,10.0)
e_arr = np.arange(0.1,1.0,0.1)
r_arr = np.arange(-40.0,500.0,20.0)
d_mg, h_mg, e_mg, r_mg = np.meshgrid(d_arr, h_arr, e_arr, r_arr)
# d_mg, h_mg = np.meshgrid(d_arr, h_arr)
print("stop")
#print(d_mg[:,0,0,0])
# for distance in :
#     for humidity in np.arange(20.0,100.0,10.0):
#         for emissivity in np.arange(0.1,1.0,0.1):
#             for reflection in np.arange(-40.0,500.0,20.0):
                