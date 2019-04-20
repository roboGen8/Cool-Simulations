from classes import *

def readStoplights(stoplight_map):
    #Since not many stoplights, just manually input
    #[GLT, YLT, RLT, GTR, YTR, Rall]
    #--> LT is left turn, Rall is basically complete stop
    east10 = [8, 1.8, 1.8, 30, 3.8, 55]
    west10 = [5, 3.6, 4.2, 28, 3.8, 55]
    north10 = [7, 3.6, 2.2, 34.7, 3.6, 49.3]
    south10 = [7, 3.6, 2.2, 34.7, 3.6, 49.3]

    east11 = [0, 0, 0, 20.2, 3.6, 76.1]
    west11 = [0, 0, 0, 20.3, 3.6, 76.2]
    north11 = [0, 0, 0, 41.5, 3.2, 55.4]
    south11 = [0, 0, 0, 41.5, 3.2, 55.4]

    east12 = [0, 0, 0, 27.3, 3.6, 69.2]
    west12 = [0, 0, 0, 27.3, 3.6, 69.2]
    north12 = [0, 0, 0, 60.9, 3.2, 35.7]
    south12 = [0, 0, 0, 61.4, 3.2, 35.7]

    east13 = [0, 0, 0, 0, 0, 0]
    west13 = [0, 0, 0, 0, 0, 0]
    north13 = [0, 0, 0, 0, 0, 0]
    south13 = [0, 0, 0, 0, 0, 0]

    east14 = [9.8, 3.6, 87, 36.9, 3.7, 60.2]
    west14 = [0, 0, 0, 22.4, 3.7, 74]
    north14 = [8.8, 3.6, 3.6, 34.6, 3.2, 46.1]
    south14 = [11.6, 3.6, 0.5, 36.6, 3.2, 45.3]

    stoplight_map[0] = Stoplight(east10, west10, north10, south10)
    stoplight_map[1] = Stoplight(east11, west11, north11, south11)
    stoplight_map[2] = Stoplight(east12, west12, north12, south12)
    stoplight_map[3] = Stoplight(east13, west13, north13, south13)
    stoplight_map[4] = Stoplight(east14, west14, north14, south14)
