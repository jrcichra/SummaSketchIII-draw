import serial
from paint import Paint
import threading
import queue

ASCII   = "za"
VERSION = "z?"
HIGHRES = "v"
SENDCONFIG = "a"
ser = serial.Serial("/dev/ttyS0",9600,parity=serial.PARITY_ODD)

def run_command(command='',read=True,prefix="",chop=False,process=False):
    if command != '':
        b = command.encode('ascii')
        ser.write(b)
        print(f"Sent: {command}")
    output = ""
    while True and read:
        char = ser.read(1)
        if char == b'\r':
            break
        output += char.decode('utf-8')
    if output != "" or prefix != "":
        if chop:
            output = output[1:]
        print(f"{prefix}{output}")
        if process:
            a = output.split(',')
            x = int(a[0])
            y = int(a[1])
            b = int(a[2])
            return (x,y,b)
        return output

run_command(command=ASCII,read=False)
run_command(command=VERSION,prefix="Version: ")
run_command(command=HIGHRES,read=False)
pw, ph, pp = run_command(command=SENDCONFIG,prefix="Resolution: ",process=True)

run_command(prefix="Ready for xy values...",read=False)

q = queue.Queue()

w = 900
ratio = pw / ph
h = w / ratio
print(f"width is {w} and height is {h} to match ratio of {ratio}")

t = threading.Thread(target=Paint, args=(w,h,q)).start()

class Position():
    def __init__(self,x,y,b):
        self.x = x
        self.y = y
        self.b = b

while True:
    x, y, b = run_command(chop=True,process=True)
    p = Position(x / (pw / w ), h - ( y / (ph / h)), b)
    #p = Position(x / 76.2, 600 - (y / 50.8), b)
    q.put(p)
