import queue
from constants import *
import random

global fin_vehicles
fin_vehicles = []

class Event:
    def __init__(self, ts, index10, index11, index12, index14):
        self.ts = ts
        self.index10 = index10
        self.index11 = index11
        self.index12 = index12
        self.index14 = index14


class FutureEventList:
    def __init__(self):
        self.q =  queue.Queue()
        self.prevEvent = None

    def push(self, evt):
        if self.prevEvent is None:
            self.q.put(evt)
            self.prevEvent = evt
        else:
            if self.prevEvent.index10 != evt.index10 or self.prevEvent.index11 != evt.index11 or self.prevEvent.index12 != evt.index12 or self.prevEvent.index14 != evt.index14:
                self.q.put(evt)
                self.prevEvent = evt

    def pop(self):
        return self.q.get()


    def is_empty(self):
        return self.q.empty()

# class Road:
#     def __init__(self):
class Vehicle:
    def __init__(self, start):
        self.start = start
        self.finished = False

    def exitVehicle(self, end):
        self.end = end
        self.finished = True


class World:
    def __init__(self):
        self.q10to11 = queue.Queue()
        self.q11to12 = queue.Queue()
        self.q12to13 = queue.Queue()
        self.q13to14 = queue.Queue()

        self.drivethru = [True, True, True, True, True] #for servers 10, 11, 12, 13, 14

    def updateServer(self, currEvent):
        count10=count11=count12=count14=0
        for i in currEvent.index10:
            if i % 3 == 0:
                count10 += 1

        for i in currEvent.index11:
            if i % 3 == 0:
                count11 += 1

        for i in currEvent.index12:
            if i % 3 == 0:
                count12 += 1

        for i in currEvent.index14:
            if i % 3 == 0:
                count14 += 1

        #probability that you can go in the server
        #Also state variables
        self.s10 = (5 - count10) / 5
        self.s11 = (5 - count11) / 5
        self.s12 = (5 - count12) / 5
        self.s13 = (5 - 4) / 5
        self.s14 = (5 - count14) / 5

    def passIntersection(self):
        out = [False, False, False, False, False] #return which servers whill allow vehicles to go through
        for i in range(len(self.drivethru)):
            if self.drivethru[i] == False:
                self.drivethru[i] = True
                out[i] = True
            else:
                #average vehicle speed from data is 4.2672m/s vs mean vehicle length of 5m
                car_prob = 4.2672 / 5.0
                if i == 0:
                    server_prob = self.s10
                elif i == 1:
                    server_prob = self.s11
                elif i == 2:
                    server_prob = self.s12
                elif i == 3:
                    server_prob = self.s13
                else:
                    server_prob = self.s14
                temp = car_prob * server_prob
                if temp >= 0.5:
                    self.drivethru[i] = True #no change
                    out[i] = True
                else:
                    self.drivethru[i] = False
                    out[i] = False
        return out




        # if self.drivethru == False:
        #     self.drivethru = True
        #     return True #let vehicle pass the Intersection
        # else:
        #     #average vehicle speed from data is 4.2672m/s vs mean vehicle length of 5m
        #     prob = 4.2672 / 5.0
        #     if num == 10:
        #         temp = prob * world.s10 * random.uniform(0, 1)





#Event Handler Procedure
def eventHandler(now, timeDif, evt, world):
    for i in range(timeDif):
        out = world.passIntersection()
        for j in range(len(out)):
            if out[j]:
                if j == 0:
                    car = Vehicle(now)
                    world.q10to11.put(car)
                elif j == 1:
                    world.q11to12.put(world.q10to11.get())
                elif j == 2:
                    world.q12to13.put(world.q11to12.get())
                elif j == 3:
                    world.q13to14.put(world.q12to13.get())
                else:
                    finCar = world.q13to14.get()
                    finCar.exitVehicle(now)
                    fin_vehicles.append(finCar)
