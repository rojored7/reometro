import threading
import time
import RPi.GPIO as GPIO


class MyPlayer(threading.Thread):

    def Channel_A(self,channel):
        if GPIO.input(self.B) == 0 :
            self.c -= 1
        else:
            self.c += 1
  
    def Channel_B(self,channel):  
        if GPIO.input(self.A) == 1 :
            self.c -= 1
        else:
            self.c += 1

    def getTime(self):
        r = time.time()*1000
        return r
    
    def __init__(self):

        # initialize the inherited Thread object
        threading.Thread.__init__(self)
        self.daemon = True

        # create a data lock
        self.my_lock = threading.Lock()

        # a variable exclusively used by thread1
        self.t1 = 0

        # a variable exclusively used by thread2
        self.t2 = 0

        # a variable shared by both threads
        self.g = 0

        self.c = 0 #Counter
        self.ppr = 5608*10
        self.ippr = 1/self.ppr
        self.pos = 0;

        self.tv = 0
        self.dtv = 0

        self.T = self.getTime()
        self.tm = 10
        self.dc = 0

        self.A = 17
        self.B = 23

        self.DirA = 27
        self.DirB = 22

        self.P = 12

        self.EnR = 19
        self.EnL = 26

        self.Pos = 0

        self.vel = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.A, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        GPIO.setup(self.B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.P, GPIO.OUT)
        GPIO.setup(self.EnR, GPIO.OUT)
        GPIO.setup(self.EnL, GPIO.OUT)
        GPIO.setup(self.DirA, GPIO.OUT)
        GPIO.setup(self.DirB, GPIO.OUT)
        GPIO.add_event_detect(self.A, GPIO.FALLING, callback=self.Channel_A)
        GPIO.add_event_detect(self.B, GPIO.FALLING, callback=self.Channel_B)


        GPIO.output(self.EnR, True)
        GPIO.output(self.EnL, True)

        GPIO.output(self.DirA, False) ##FALSE
        GPIO.output(self.DirB, True)
        
        self.pw = GPIO.PWM(self.P,1000)
        self.pw.start(20)

        # start thread 1
        self.thread1()

    def thread1(self):
        # start the 2nd thread
        # you must start the 2nd thread using the name "start"
        self.start()
        while True:

            if (self.getTime() - self.T >= self.tm):
                self.Pos = self.c*self.ippr
                self.c = 0
                self.dtv = self.getTime() - self.tv
                self.vel = self.Pos*1000/self.dtv
                self.tv = self.getTime()
                self.T = self.getTime()

    def run(self):
        """
        This the second thread's executable code. It must be called run.
        """
        while True:
            #with self.my_lock:
            #    self.t2 += 1
            #    self.g = self.t1 + self.t2

            print('vel:{0:4.5f} Pos:{1:5.4f} dtv:{2:5.2f}'.format(self.vel, self.Pos, self.dtv))


MyPlayer()
