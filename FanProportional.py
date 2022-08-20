import RPi.GPIO as IO          #Calling GPIO to allow use of the GPIO pins
import time                    #Calling time to allow delays to be used
import subprocess              #Calling subprocess to get the CPU temperature

IO.setwarnings(False)          #Do not show any GPIO warnings
IO.setmode (IO.BCM)            #BCM pin numbers - PIN8 as ‘GPIO14’
IO.setup(14,IO.OUT)            #Initialize GPIO14 as our fan output pin
fan = IO.PWM(14,100)           #Set GPIO14 as a PWM output, with 50Hz frequency (this should match your fans specified PWM frequency)
fan.start(0)                   #Generate a PWM signal with a 0% duty cycle (fan off)

minTemp = 25
maxTemp = 80
minSpeed = 0
maxSpeed = 100

def get_temp():                #Function to read in the CPU temperature and return it as a float in degrees celcius
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

while 1:                                     #Execute loop forever
    temp = get_temp()                        #Get the current CPU temperature
    if temp < minTemp:
        temp = minTemp
    elif temp > maxTemp:
        temp = maxTemp
    temp = int(renormalize(temp, [minTemp, maxTemp], [minSpeed, maxSpeed]))
    fan.ChangeDutyCycle(temp)               #Set fan duty based on temperature, from 0% (off) to 100% (full speed)
    time.sleep(5)                           #sleep for 5 seconds