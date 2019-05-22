from data_helper import *
from data_classes import *
from data_vars import *

#Read data
global place_set

global vehicle_map
global stoplight_map
vehicle_map = dict()
stoplight_map = dict()

readStoplights(stoplight_map, "stoplight.csv")
readVehicles(vehicle_map, "trajectories-0400pm-0415pm_editted.csv")

# coun = 0
# for i in range(753):
#     v = vehicle_map[i]
#     if abs(v.Global_X[0] - 2230542) <= 10 and abs(v.Global_X[len(v.Global_X) - 1] - 2230806) <= 10:
#         if abs(v.Global_Y[0] - 1375766) <= 10 and abs(v.Global_Y[len(v.Global_Y) - 1] - 1377542) <= 10:
#             coun+=1
# print(coun)

#Count how many cars initially
count = 0
v1 = vehicle_map[0]
tupSet = dict()
for i in range(50, 1630):
    tupSet[int(v1.Global_X[i])] =int(v1.Global_Y[i])

for i in range(1, 753):
    if int(vehicle_map[i].Global_X[0]) in tupSet:
        if tupSet[int(vehicle_map[i].Global_X[0])] == int(vehicle_map[i].Global_Y[0]):
            count+=1


print(count)
