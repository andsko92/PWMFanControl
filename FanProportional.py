import RPi.GPIO as gpio          
import time                    
import subprocess              

gpio_pin = 18
freq = 100
minTemp = 35                   
maxTemp = 80
minSpeed = 0
maxSpeed = 100

gpio.setwarnings(False)          
gpio.setmode(gpio.BCM)            
gpio.setup(gpio_pin,gpio.OUT)            
fan = gpio.PWM(gpio_pin,freq)           
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
    fan.ChangeDutyCycle(temp)
    time.sleep(5)       
