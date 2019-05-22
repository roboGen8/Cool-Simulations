import queue
from constants import *
import random

global INITIAL_VEH #Initial number of vehicles in the road segments
#probablity is obtained from estimated number of vehicles entering server10
#from the NGSIM data divided by total amount of simulation time 900s
global ENTER_PROB #Calculated for 10th intersection was 0.13
global SERVER_PROB #default is 0.25
global CAR_PROB

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
    def __init__(self, start, type):
        self.start = start
        self.finished = False
        self.type = type #True if came from 10th intersection

    def exitVehicle(self, end):
        self.end = end
        self.finished = True
        self.time = self.end - self.start + 20


class World:
    def __init__(self):
        self.q10to11 = queue.Queue()
        self.q11to12 = queue.Queue()
        self.q12to13 = queue.Queue()
        self.q13to14 = queue.Queue()

        #Initialize world with some cars in the roads:
        for i in range(INITIAL_VEH):
            self.q10to11.put(Vehicle(0, False))
            self.q11to12.put(Vehicle(0, False))
            self.q12to13.put(Vehicle(0, False))
            self.q13to14.put(Vehicle(0, False))

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
        self.s10 = (5 - count10) * SERVER_PROB
        self.s11 = (5 - count11) * SERVER_PROB
        self.s12 = (5 - count12) * SERVER_PROB
        self.s13 = (5 - 3) * SERVER_PROB
        self.s14 = (5 - count14) * SERVER_PROB


    def passIntersection(self):
        out = [False, False, False, False, False] #return which servers whill allow vehicles to go through
        for i in range(len(out)):
            if i == 0:
                server_p = self.s10
            elif i == 1:
                server_p = self.s11
            elif i == 2:
                server_p = self.s12
            elif i == 3:
                server_p = self.s13
            else:
                server_p = self.s14
            temp = CAR_PROB * server_p
            if random.uniform(0, 1) <= temp:
                out[i] = True
            else:
                out[i] = False
        return out


#Event Handler Procedure
def eventHandler(now, timeDif, evt, world, fin_vehicles):
    for i in range(timeDif):
        #checks if the server allows pass through but still have to check stop light is not red
        out = world.passIntersection()
        #adding to 10to11 queue
        if random.uniform(0, 1) <= ENTER_PROB[0]:
            if world.q10to11.qsize() < from10to11:
                car = Vehicle(now, True)
                world.q10to11.put(car)
        for j in range(1, len(out)):
            if out[j]:
                if j == 1:
                    #Make sure there is a car in 10to11 road
                    if not world.q10to11.empty():
                        #Make a decision if turn left or straight
                        turn_or_straight = random.uniform(0, 1)
                        if turn_or_straight <= (6+12.5) / from10to11: #wants to go left or right
                            if evt.index11[2] != 2 and evt.index11[2] != 5:
                                deq_car = world.q10to11.get()
                        else: #wants to go straight
                            if evt.index11[2] == 3 or evt.index11[2] == 4:
                                if world.q11to12.qsize() < from11to12:
                                    deq_car = world.q10to11.get()
                                    world.q11to12.put(deq_car)
                    #Adding cars coming from west and east
                    from_sides = random.uniform(0, 1)
                    if from_sides <= (2.0 * ENTER_PROB[1] / 3.0):
                        if world.q11to12.qsize() < from11to12:
                            side_car = Vehicle(now, False)
                            world.q11to12.put(side_car)

                elif j == 2:
                    if not world.q11to12.empty():
                        turn_or_straight = random.uniform(0, 1)
                        if turn_or_straight <= (9+12) / from11to12:
                            if evt.index12[2] != 5:
                                deq_car = world.q11to12.get()
                        else:
                            if evt.index12[2] != 5:
                                if world.q12to13.qsize() < from12to13:
                                    deq_car = world.q11to12.get()
                                    world.q12to13.put(deq_car)
                    from_sides = random.uniform(0, 1)
                    if from_sides <= (2.0 * ENTER_PROB[2] / 3.0):
                        if world.q12to13.qsize() < from12to13:
                            side_car = Vehicle(now, False)
                            world.q12to13.put(side_car)

                elif j == 3:
                    if not world.q12to13.empty():
                        turn_or_straight = random.uniform(0, 1)
                        if turn_or_straight <= (11) / from12to13:
                            deq_car = world.q12to13.get()
                        else:
                            if world.q13to14.qsize() < from13to14:
                                deq_car = world.q12to13.get()
                                world.q13to14.put(deq_car)
                    from_sides = random.uniform(0, 1)
                    if from_sides <= (1.0 * ENTER_PROB[3] / 3.0):
                        if world.q13to14.qsize() < from13to14:
                            side_car = Vehicle(now, False)
                            world.q13to14.put(side_car)

                elif j == 4:
                    if not world.q13to14.empty():
                        if evt.index14[2] != 2 and evt.index14[2] != 5:
                            finCar = world.q13to14.get()
                            finCar.exitVehicle(now)
                            if finCar.type == True:
                                fin_vehicles.append(finCar)
