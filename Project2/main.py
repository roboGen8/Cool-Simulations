
from engine import *
import time
from constants import *
list_avetime = []
list_passed = []

def main():
    #Future Event List
    fel = FutureEventList()


    #Make Future Event List
    #Based on 15mins/900 seconds given and stoplight data
    for t in range(1, 901):
        index10=index11=index12=index14 = [0, 0, 0, 0]
        stop10 = [east10, west10, north10, south10]
        stop11 = [east11, west11, north11, south11]
        stop12 = [east12, west12, north12, south12]
        stop14 = [east14, west14, north14, south14]
        tval10 = [t%sum(east10), t%sum(west10), t%sum(north10), t%sum(south10)]
        tval11 = [t%sum(east11), t%sum(west11), t%sum(north11), t%sum(south11)]
        tval12 = [t%sum(east12), t%sum(west12), t%sum(north12), t%sum(south12)]
        # tval13 = [t%sum(east13), t%sum(west13), t%sum(north13), t%sum(south13)]
        tval14 = [t%sum(east14), t%sum(west14), t%sum(north14), t%sum(south14)]


        for i in range(4):
            count = 0
            for j in range(6):
                if tval10[i] > sum((stop10[i])[0:j+1]):
                    count+=1
            index10[i] = count


        for i in range(4):
            count = 0
            for j in range(6):
                if tval11[i] > sum((stop11[i])[0:j+1]):
                    count+=1
            index11[i] = count

        for i in range(4):
            count = 0
            for j in range(6):
                if tval12[i] > sum((stop12[i])[0:j+1]):
                    count+=1
            index12[i] = count

        for i in range(4):
            count = 0
            for j in range(6):
                if tval14[i] > sum((stop14[i])[0:j+1]):
                    count+=1
            index14[i] = count


        event = Event(t, index10, index11, index12, index14)
        fel.push(event)



    #Time statistics
    start_time = time.time()
    NEvents = 0

    #Event Processing Loop
    world = World()
    fin_vehicles = []
    now = 0
    # print("Now: " + str(now) + "\n")
    # print("|10th|===" + str(world.q10to11.qsize()) + "===|11th|===" +  str(world.q11to12.qsize()) + "===|12th|===" +  str(world.q12to13.qsize()) + "===|13th|===" + str(world.q13to14.qsize()) + "===|14th|" +"\n")
    while not fel.is_empty():
        currEvent = fel.pop()

        world.updateServer(currEvent)
        timeDif = currEvent.ts - now
        now = currEvent.ts
        eventHandler(now, timeDif, currEvent, world, fin_vehicles)
        # print("Now: " + str(now) + "\n")
        # print("|10th|===" + str(world.q10to11.qsize()) + "===|11th|===" +  str(world.q11to12.qsize()) + "===|12th|===" +  str(world.q12to13.qsize()) + "===|13th|===" + str(world.q13to14.qsize()) + "===|14th|" +"\n")


    vehicle10to14 = 0
    passtime = []
    for vehicle in fin_vehicles:
        if vehicle.type == True and vehicle.finished == True:
            vehicle10to14 += 1
            passtime.append(vehicle.time)
            # print(str(vehicle10to14) + ": " + str(vehicle.time) + "seconds")

    # print("There are: " + str(vehicle10to14) + " vehicles that travelled from 10th to 14th")
    end_time = time.time()
    list_avetime.append(sum(passtime)/len(passtime))
    list_passed.append(vehicle10to14)

if __name__ == '__main__':
    for i in range(10):
        INITIAL_VEH = 50
        ENTER_PROB = [random.uniform(0.1), 0.30, 0.30, 0.15, 0.12]
        SERVER_PROB = 0.2
        CAR_PROB = 4.42 / 5.0
        main()
    # print("\n")
    # print("List of simulation average time in seconds:")
    # print(list_avetime)
    # print("-------------------")
    # print("List of the number of vehicles that travelled from 10th to 14th:")
    # print(list_passed)
