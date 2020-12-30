import RPi.GPIO as GPIO
import time
import threading
from socket import *

#pin definitions

DIRECTION = 22
STEP = 23
pwm = 50


#setup GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIRECTION ,GPIO.OUT)
GPIO.setup(STEP ,GPIO.OUT)

nema17 = GPIO.PWM(STEP, 1500)
nema17.start(pwm)
GPIO.output(DIRECTION, GPIO.LOW)



ctrCmd = ["CW", "CCW", "ACC", "DEACC"]
HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST,PORT)
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)



def handle_client(tcpCliSock,addr):
        print ('...connected from:', addr)
        try:
                while True:
                        data = tcpCliSock.recv(BUFSIZE)
                        data = data.decode('utf-8') 
                        
                        if data == ctrCmd[0]:
                                print("CW")
                                time.sleep(2)
                                GPIO.output(DIRECTION, GPIO.LOW)
                        if data == ctrCmd[1]:
                                print("CCW")
                                time.sleep(2)
                                GPIO.output(DIRECTION, GPIO.HIGH)
                        if data == ctrCmd[2]:
                                print("ACC")
                                global pwm
                                if pwm < 100:
                                        pwm = pwm + 5
                                nema17.start(pwm)
                                print(pwm)
                        if data == ctrCmd[3]:
                                print("DEACC")
                                if pwm > 0:
                                        pwm = pwm - 5
                                nema17.start(pwm)
                                print(pwm)
                        
                        
        except KeyboardInterrupt:
                GPIO.cleanup()
                tcpSerSock.close()
                
                

def start():
        print("Waiting for connection...")
        tcpSerSock.listen()
        while True:
                tcpCliSock,addr = tcpSerSock.accept()
                thread = threading.Thread(target=handle_client, args=(tcpCliSock,addr))
                thread.start()        
        

start()
                
        


