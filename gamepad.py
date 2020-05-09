import pygame
import serial

def init_serial(port="COM26", baud=115200):
    ser = serial.Serial(port, baud, timeout=1)
    # open the serial port
    if ser.isOpen():
        print(ser.name + ' is open...')
    return ser

def send_message(ser, message, servo):
    message = str(message) + servo
    print(message)
    for char in message:
        ser.write(bytes(char, 'ascii'))
    if ser.readable():
        out = ser.read_until()
        print('Receiving... ' + str(out, 'ascii'))

def constraint(val, up_lim, bot_lim):
    if val > up_lim:
        return up_lim
    elif val < bot_lim:
        return bot_lim
    else:
        return val

def main():

    step = 1.5
    shift = 0
    mess_key = {
      0: [97, 1],
      1: [98, 1],
      2: [97, -1],
      3: [98, -1]
    }
    prev_button = []
    servo = {}
    for i in range(16):
        servo[chr(97+i)] = 90
    # init gamepad
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    sp = init_serial()
    
    buttons = j.get_numbuttons()
    for i in range(buttons):
        prev_button.append(0)
##    axes = j.get_numaxes()
##    hats = j.get_numhats()
    while True:
        pygame.event.pump()
        for i in range(buttons):
            button = j.get_button(i)
            if button:
                if i == 7:
                    if prev_button[i] != button:
                        shift = constraint(shift+1, 15, 0)
                        print('shift', shift)
                elif i == 5:
                    if prev_button[i] != button:
                        shift = constraint(shift-1, 15, 0)
                        print('shift', shift)
                elif i == 6:
                    if prev_button[i] != button:
                        step = constraint(step+0.1, 10, 0)
                        print('step', step)
                elif i == 4:
                    if prev_button[i] != button:
                        step = constraint(step-0.1, 10, 0)
                        print('step', step)
                else:
                    print('button pressed', i)
                    servo_key = chr(mess_key[i][0] + shift)
                    servo[servo_key] = constraint(servo[servo_key] + mess_key[i][1]*step, 180, 0)
                    angle = int(servo[servo_key])
                    send_message(sp, angle, servo_key)
                    # print(int(servo[chr(mess_key[i][0])]), chr(mess_key[i][0]))
            prev_button[i] = button
main()
    
