from functions import *
import matplotlib.pyplot as plt

tsdk = TSDK(verbose=0)
tsdk.load_rjpg(path="input/air_original.JPG")

e_precission = 0.01
e_start = 0.85
e_stop = 1
r_precission = 1
r_start = 20
r_stop = 30
d_list = [10.0]
h_list = [77.0]
e_list = list(np.arange(e_start,e_stop,e_precission, dtype=np.float32))
r_list = list(np.arange(r_start,r_stop,r_precission, dtype=np.float32))
sweep_temp_data = tsdk.sweep(d_list,h_list,e_list,r_list)

plt.imshow(temp_data, cmap="viridis")
plt.show()