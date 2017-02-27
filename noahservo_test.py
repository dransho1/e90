import servotest as vc

def main():
    throttle = 50
    servo = vc.ServoController()
    servo.setAngle(0, 180)
    servo.setPosition(1, 1500 + 2*throttle)

main()
