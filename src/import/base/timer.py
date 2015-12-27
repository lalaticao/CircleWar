#timer.py

"""
[Timer]
  USAGE
    Create a new timer, an instance of Timer:
      Timer([interval=1, [name="", [...]]])
        - the new timer will note every <interval> seconds when running,
          calling method <check> to check if the timer has ever noted
        - <name> is the name of the new timer, "" if not given.
        - if you want to bind functions to the new timer, add the funtions
          at the last of the list of arguments. The functions should receive
          a Timer object, for example:
          def onTimer(timer):
              pass
          They are called every time the timer notes while being checked.
          
    Run a timer:
      timer.run([times])
        - the timer will stop after it has noted <times> times
        - if <times> not given, it will run until be stopped
        - raise an exception when the timer is already running
    Stop a timer:
      timer.stop()
        - also empty the marks so that the timer will say False when checked
    Get the state of the timer:
      timer.isRunning() -> bool
        - return True if the timer is running, else return False

    Check if the timer has noted:
      timer.check() -> bool
        - return True if the timer has noted, and then take away a mark.
        - return False if there is no mark
        - the timer will make a mark every interval seconds
        - it will also call the functions binded to the timer
        - it can return True even the timer is not running only when it
          stopped naturally and there remains some marks not taken away.

    Get how long it is since the timer started running:
      timer.timeFromLastStart() -> float
        - raise an exception when the timer is not running
    Get how many times the timer has noted after the most recent call of run:
      timer.getFinish() -> int
        - raise an exception when the timer is not running
    Get how many times the timer has to note then before stopped naturally:
      timer.getRemain() -> int
        - raise an exception when the timer is not running
        
    Get and change the name of the timer:
      timer.name
        - do whatever you want to do with its name :-)
    Get the interval of the timer:
      timer.getInterval() -> int or float
    Set a new interval:
      timer.setInterval(interval)
        - the interval should be positive
        
    Bind functions to the timer:
      timer.bind(...)
        - the same functions will only be called once
    Unbind functions:
      timer.unbind(...)

  EXAMPLE 1
    timer = Timer(100, "mytimer")
    timer.run(1)
    ... #operations
    if timer.check():
        print "too slow."
    else:
        print "cool."
        
  EXAMPLE 2
    timer = Timer(1.0/60, "frame")
    timer.run()
    while True:
        if timer.check():                     # code like this, with the timer,
            for graph_object in object_list:  # for example you can move the
                graph_object.move()           # graphs once every frame.
                
        ... # handle the input of mouse and keyboard
        
        if game.isOver():   # judge
            timer.stop()
            break
    print "gameover"
    
[TimerSet]
Set for timers.
  USAGE
    create a new set and add timers to it or remove timers from it just by the
    same way as operating a normal set.
    specially to create a new timer in the set, use method createTimer:
      timerset.createTimer(interval, [name, [...]]) -> Timer
        -it will return the timer created right now
  EXAMPLE
    ts = TimerSet()
    ts.createTimer(1.0/60, "frame").run(240)
    ts.createTimer(1, "second").run()
    #getFinish raise exception when the timer is stopped
    try:
        while True:
            for timer in ts:
                if timer.check():
                        print timer.getFinish(), timer.name
    except TimerError:pass
    for timer in ts:
        print timer.name, timer.isRunning()
"""

import time

class TimerError(Exception):
    pass
class TimerSetError(Exception):
    pass

class Timer:
    def __init__(self, interval=1, name="", *func):
        self.name = name
        self.setInterval(interval)
        self.stop()
        
        self._func = []
        self.bind(*func)

    def __str__(self):
        s="Timer <"+self.name+">\n  interval: "+str(self._interval)+"s\n  "
        if self._running and self._run_times < 0:
            s+="running forever, %d times finished.\n"%self.getFinish()
        elif self._running:
            s+="running, %d times remaining, %d times finished.\n"\
                  %(self.getRemain(),self.getFinish())
        else:
            s+="stopped.\n"
        return s
    def bind(self, *func):
        for f in func:
            if not(f in self._func):
                self._func += [f]
    def unbind(self, *func):
        for f in func:
            if f in self._func:
                self._func.remove(f)
    
    def setInterval(self, interval):
        if interval <= 0:
            raise TimerError("interval should be positive")
        self._interval = interval
    def getInterval(self):
        return self._interval
    
    def isRunning(self):
        return self._running
    def run(self, times=-1):
        if self._running:
            raise TimerError("Timer "+self.name+" is running.")
        self._running = True
        self._run_times = times
        self._remaining_times = times
        self._finish_times = 0
        self._start_clock = time.clock()
        self._last_start_clock = self._start_clock
    def stop(self):
        self._running = False
        self._finish_times = 0

    def timeFromLastStart(self):
        if not (self._running or self._finish_times):
            raise TimerError("Timer "+self.name+" is not running.")
        return time.clock() - self._last_start_clock
    
    def getRemain(self):
        if self._running or self._finish_times:
            return -1 if self._run_times < 0 else self._remaining_times
        else:
            raise TimerError("Timer "+self.name+" is not running.")
    def getFinish(self):
        if self._running or self._finish_times:
            return self._run_times - self._remaining_times
        else:
            raise TimerError("Timer "+self.name+" is not running.")

    def check(self):
        if self._running:
            if self._remaining_times == 0:
                self._running = False
            else:
                curclock = time.clock()
                times=(curclock - self._start_clock)/self._interval
                if self._run_times > 0 and times >= self._remaining_times:
                    self._finish_times += self._remaining_times
                    self._remaining_times=0
                elif times >=1:
                    self._remaining_times -= int(times)
                    self._finish_times += int(times)
                    self._start_clock = curclock
        if self._finish_times > 0:
            self._finish_times = 0
            for f in self._func:
                f(self)
            return True
        return False


class TimerSet(set):
    def createTimer(self, interval=1, name="", *func):
        timer = Timer(interval, name, *func)
        self.add(timer)
        return timer
    def add(self, *timers):
        for timer in timers:
            if not isinstance(timer, Timer):
                raise TimerSetError("the element of the timerset should "+\
                                    "be a timer(an object of class Timer)")
        set.add(self,*timers)
    def bind(*func):
        for timer in self:
            timer.bind(*func)
    def unbind(*func):
        for timer in self:
            timer.unbind(*func)



def _onTimerTest(timer):
    print "    ##################"
    print "    # binded function#"
    print "    # Timer", timer.name
    print "    #",timer.getFinish(),timer.getRemain()
    print "    #",timer.getInterval()
def test():
    t1=Timer(1.0/60,"f")
    t1.run(60)
    t1.bind(_onTimerTest)
    t2=Timer(1,"1s")
    t2.run(1)
    while True:
        if t1.check():
            print t1.getFinish()
        if t2.check():
            print t2.getFinish()
            break
    
    ts=TimerSet()
    ts.createTimer(1,"onesecond").run()
    ts.createTimer(10,"tensecond",_onTimerTest).run(3)
    ts.createTimer(30,"halfminute").run(1)
    
    while True:
        for timer in ts:
            if timer.check():
                print "!!!",timer.name,"!!!"
                if timer.name=="onesecond":
                    if timer.getFinish()==35:
                        return
                    for i in ts:
                        print i
if __name__ == "__main__":
    test()

        
