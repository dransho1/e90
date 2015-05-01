import cv2
FILE = 'foo.mp4'

vc = cv2.VideoCapture(FILE)

while(True):
    ret, frame = vc.read()
    if not ret:
        vc = cv2.VideoCapture(FILE)
    else:
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vc.release()
cv2.destroyAllWindows()
