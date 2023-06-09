import cv2
import numpy as np
import os
import serial


def arduino_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('dataset/trainer.yml')
cascadePath = "classifier/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Padrone']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

x_delta = 50
y_delta = 45

while True:

    ret, img = cam.read()
    # img = cv2.flip(img, -1)  # Flip vertically

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #equalized_image = cv2.equalizeHist(gray)
    normalised_image = np.zeros((300, 300))
    imageNp = cv2.normalize(gray, normalised_image, 0, 255, cv2.NORM_MINMAX)

    faces = faceCascade.detectMultiScale(
        imageNp,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:

        #cv2.rectangle(imageNp, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        id, confidence = recognizer.predict(imageNp[y:y + h, x:x + w])


        if id == 1:
            # id = names[id]
            #distance = round(158 - 0.43 * ((w + h) / 2))
            mid_x = x + w / 2
            mid_y = y + h / 2

            turn = 0
            acc = 0

            if mid_x < (640 / 2 - x_delta) or mid_x > (640 / 2 + x_delta):
                turn = int(-1 *arduino_map((mid_x - (640 / 2 + x_delta)), -640/2 + x_delta, 640/2 - x_delta, -50, 50))

            if mid_y < (480 / 2 - y_delta) or mid_y > (480 / 2 + y_delta):
                acc = int(arduino_map((mid_y - (480 / 2 + y_delta)), -480/2 + y_delta, 480/2 - y_delta, -75, 75))

            string = str(acc) + "," + str(turn) + ",100\n"
            ser.write(string.encode('utf-8'))
            print(string)
        '''
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            distance = round(158 - 0.43 * ((w + h) / 2))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            distance = round(158 - 0.43 * ((w + h) / 2))

        cv2.putText(imageNp, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(imageNp, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        # cv2.putText(img, f'Distance: {distance}', (x - 10, y + h - 5), font, 1, (255, 0, 255), 2)

    cv2.imshow('camera', imageNp)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break
        '''

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
