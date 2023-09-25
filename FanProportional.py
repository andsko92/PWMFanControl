import RPi.GPIO as gpio          
import time                    
import subprocess              

gpioPin = 18
freq = 25
minTemp = 45                   
maxTemp = 80
minSpeed = 0
maxSpeed = 100
speedFactor = 1.5

gpio.setwarnings(False)          
gpio.setmode(gpio.BCM)            
gpio.setup(gpioPin,gpio.OUT)            
fan = gpio.PWM(gpioPin,freq)           
fan.start(0)

def get_temp():                             
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not get temperature')
    
def renormalize(n, range1, range2):         
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]

while True:                                    
    temp = get_temp()                       
    if temp < minTemp:
        temp = minTemp
    elif temp > maxTemp:
        temp = maxTemp
    temp = int(renormalize(temp, [minTemp, maxTemp], [minSpeed, maxSpeed]))
    if temp > (maxSpeed / speedFactor):
        fan.ChangeDutyCycle(temp)
    else:
        fan.ChangeDutyCycle(temp*speedFactor)
    time.sleep(5)       
