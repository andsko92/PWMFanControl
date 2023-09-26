import RPi.GPIO as gpio          
import time                    
import subprocess              

gpioPin = 18
freq = 25
minSpeed = 0
maxSpeed = 100

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

while True:                                     
    temp = get_temp()                        
    if temp > 80:                            
        fan.ChangeDutyCycle(100)
    elif temp > 75:
        fan.ChangeDutyCycle(90)
    elif temp > 70:
        fan.ChangeDutyCycle(80)
    elif temp > 65:
        fan.ChangeDutyCycle(70)
    elif temp > 60:
        fan.ChangeDutyCycle(60)
    elif temp > 55:
        fan.ChangeDutyCycle(55)
    elif temp > 50:
        fan.ChangeDutyCycle(40)
    elif temp > 45:
        fan.ChangeDutyCycle(30)
    else:
        fan.ChangeDutyCycle(0)
    time.sleep(5)                            
