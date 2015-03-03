import servotest as sc
SAFETY = 0
MOTOR_NEUTRAL = 1500
ESC_SERVO = 1
STEER_SERVO = 0

def cvtThrot(throt):
    if throt >= 128:
        return throt % 128
    else:
        return throt + 129
# Open the js0 device as if it were a file in read mode.
pipe = open('/dev/input/js0', 'r')

# Create an empty list to store read characters.
msg = []

esc_val = MOTOR_NEUTRAL
# Loop forever.

control = sc.ServoController()
while 1:
    print "Motor value", esc_val
    for char in pipe.read(1):
        msg += [ord(char)]
        if len(msg) == 8:
            if msg[6] == 1:
                if msg[4]  == 1:
                    print 'button', msg[7], 'down'
                else:
                    print 'button', msg[7], 'up'
            elif msg[6] == 2:
                if int(msg[7]) == 0:
                    steering_val = int(msg[5])
                    if steering_val in range(0,128):
                        steering_angle = 90-steering_val*(90.0/127)
                    else:
                        steering_angle = 90+(255-steering_val)*(90.0/127)
                    if steering_angle > 180-SAFETY:
                        steering_angle = 180-SAFETY
                    elif steering_angle < SAFETY:
                        steering_angle = SAFETY
                    print steering_angle
                    control.setAngle(STEER_SERVO, steering_angle)
                else:
                    forwar_throt = None
                    rev_throt = None
                    print "axis", msg[7]
                    if int(msg[7]) == 5:
                        #Forward Throttle
                        forward_throt = int(msg[5])
                        forward_throt = cvtThrot(forward_throt)
                        print "forward", forward_throt 
                    if int(msg[7]) == 2:
                        #reverse throttle
                        rev_throt = cvtThrot(int(msg[5]))
                        print "reverse", rev_throt
                    try:
                        if rev_throt:
                                #reverse defeats forward
                            esc_val = MOTOR_NEUTRAL - int(2*rev_throt)
                        elif forward_throt:
                            esc_val = MOTOR_NEUTRAL + int(2*forward_throt)
                        else:
                            esc_val = MOTOR_NEUTRAL
                    except Exception as e:
                        print "Exception", str(e)
                        pass
            
            msg = []
            control.setPosition(ESC_SERVO, esc_val)


