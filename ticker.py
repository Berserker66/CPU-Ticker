#!/usr/bin/env python3
from multiprocessing import Pool, freeze_support
import gui
import time
from shared import Settings

def lin(start, rel, delta):
    return start+rel*delta

def timestress(name, start_time, settings, end_time):
    cycletime = 1/settings.frequency
    busytime = cycletime/2

    while start_time > time.time():
        pass#busy wait
    start_time = time.clock()
    while time.time() < end_time:
        while time.clock()-start_time < busytime:
            pass

        start_time += cycletime
        time.sleep(max(0,start_time-time.clock()))

def linfreqstress(name, start_time, settings, end_time):
    basecycletime = 1/settings.frequency
    deltatime = (1/settings.frequency2)-basecycletime#total delta change of time
    avgcycletime = basecycletime+0.5*deltatime
    totaltime = settings.testtime

    while start_time > time.time():pass#busy wait

    start_clock = time.clock()
    x = 0
    while time.time() < end_time:
        rel = 1-((end_time-(start_time+avgcycletime*x))/totaltime)
        cycletime = basecycletime+deltatime*rel
        while time.clock()-start_clock < cycletime/2:
            pass
        start_clock += cycletime
        x+=1
        time.sleep(max(0,start_clock-time.clock()))


#timestress = linfreqstress

def timestress_debug(name, start_time, settings, end_time):
    busytime = settings.cycletime/2
    cycletime = settings.cycletime

    while start_time > time.time():
        pass#busy wait
    start_time = time.clock()
    while time.time() < end_time:
        while time.clock()-start_time < busytime:
            pass

        end = time.clock()
        print("{}: {:%} deviation.".format(name, 1-(busytime/(end-start_time))))

        start_time += cycletime
        start_sleep = time.clock()
        slep = start_time-time.clock()
        time.sleep(max(0,slep))
        if not max(0,slep):
            print((time.clock()-start_sleep)-slep)

def test(settings, update_func):
    pool2 = Pool(settings.cpucount)
    teststart = time.time()+1
    results = []
    print("Starting run.")
    stressfunc = timestress if settings.method == 0 else linfreqstress
    for x in range(settings.cpucount):
        results.append(
            pool2.apply_async(stressfunc, ("Process("+str(x)+")", teststart, settings, settings.testtime+teststart)))
    while time.time() < teststart+settings.testtime:
        update_func(time.time()-teststart) # TODO update in between
        time.sleep(0.5)
    for result in results:
        result.get()
    print("Run finished.")

if __name__ == "__main__":
    freeze_support()
    settings = Settings()
    gui.start(settings)
