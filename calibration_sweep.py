from utils import *
import matplotlib.pyplot as plt

tsdk = TSDK(verbose=0)
tsdk.load_rjpg(path="input/DJI_20211215121810_0191_T.JPG")

e_precission = 0.001
e_start = 0.94
e_stop = 0.96
#r_precission = 1
#r_start = 20
#r_stop = 30
d_list = list(np.arange(1,25,1, dtype=np.float32))
h_list = [50.0]
e_list = [0.95]
r_list = [5.0]
configurations = tsdk.sweep_setup(d_list,h_list,e_list,r_list)
tsdk.sweep_run()
mask_path = "input/mask.JPG"
mean_temps = tsdk.mask_temp_from_sweep_data(mask_path)
x_arr = []
y_arr = []
for configuration, mean_temp in zip(configurations,mean_temps):
    x_arr.append(configuration[0])
    y_arr.append(mean_temp)
for x,y in zip(x_arr,y_arr):
    print(x,y)
plt.plot(x_arr,y_arr)
plt.show()
print("stop")
#tsdk.sweep_save_tifs("output/tifs/DJI_20211215121810_0191_T")

#plt.imshow(temp_data, cmap="viridis")
#plt.show()