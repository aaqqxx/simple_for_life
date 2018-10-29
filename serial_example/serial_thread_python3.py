import serial
import threading
import time

x = serial.Serial('COM1', 9600,timeout=1000000)


# i=0
def fasong():
    while True:
        # print("wocao")
        myinput = input('shuru>')
        myinput = myinput.encode(encoding="utf-8")
        # print("you input "+myinput)
        x.write(myinput)
        time.sleep(0.1)


def jieshou():
    myout = ""
    while True:
        while x.inWaiting() > 0:
            myout += x.read(1).decode()
        if myout != "":
            print(myout)
            myout = ""
        # myout=x.read(14)
    # myout="lll"
    # time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=jieshou, name="jieshou")
    t2 = threading.Thread(target=fasong, name="fasong")
    t2.start()
    t1.start()
