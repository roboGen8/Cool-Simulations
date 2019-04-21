
from engine import *
import time
from constants import *





# #Read data
# global stoplight_map
# stoplight_map = dict()
# readStoplights(stoplight_map)

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
now = 0
while not fel.is_empty():
    currEvent = fel.pop()
    world.updateServer(currEvent)
    timeDif = currEvent.ts - now
    now = currEvent.ts
    eventHandler(timeDif, currEvent, world)

end_time = time.time()
print(end_time - start_time)
# print(fel.q.qsize())
