import pygame
import time
import serial

pygame.init()
pygame.joystick.init()

done = False


started = False

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

while not done:
    pygame.event.get()
    joystick_count = pygame.joystick.get_count()

    if joystick_count < 1:
        print('Joystick not found')
        pygame.quit()


    if not started: 
        print('%s joystick(s) found:' %joystick_count)
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            name = joystick.get_name()
            joystick_id = joystick.get_id()
            print('Name: %s, ID: %s' %(name, joystick_id))
        started = True
        time.sleep(4)
        

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    #print(joystick.get_name())
    x = -int(joystick.get_axis(0)*50)
    y = int(joystick.get_axis(1)*100)
    string = str(y) + "," + str(x) + ",100\n"
    ser.write(string.encode('utf-8'))
    print("acc: " + str(y) + " - turn: " + str(x))
    time.sleep(0.05)
