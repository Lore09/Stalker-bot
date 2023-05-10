import picamera
import numpy as np
import face_recognition
import time

def arduino_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == '__main__':
    #dist = Distance(real_distance = 48, real_width = 16)

    # Get a reference to webcam #0 (the default one)
    camera = picamera.Picamera()
    camera.resolution(720, 480)
    output = np.empty((480, 720, 3), dtype=np.uint8)

    # Load a first sample picture and learn how to recognize it.
    davide_image = face_recognition.load_image_file("ref_image.jpg")
    davide_face_encoding = face_recognition.face_encodings(davide_image)[0]

    # Load a second sample picture and learn how to recognize it.
    lorenzo_image = face_recognition.load_image_file("ref_image_2.jpg")
    lorenzo_face_encoding = face_recognition.face_encodings(lorenzo_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        davide_face_encoding,
        lorenzo_face_encoding
    ]
    known_face_names = [
        "Davide",
        "Lorenzo"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    prev_time = 0
    x_delta = 50
    y_delta = 45

    while(True):
        # Grab a single frame of video
        camera.capture(output, format="rgb")
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        face_encodings = face_recognition.face_encodings(output, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

        #distances = dist.get_distances(bounding_boxes=face_locations)

        #print(face_names)

        if len(face_names) > 0 and face_names[0] != 'Unknown':
            mid_x = 4*face_locations[0][3] + (4*face_locations[0][1] - 4*face_locations[0][3])/2  # resize *4, left + (right - left)/2
            mid_y = 4*face_locations[0][0] + (4*face_locations[0][2] - 4*face_locations[0][0])/2  # resize *4, top + (bottom - top)/2
            #print(mid_x, mid_y)

            turn = 0
            acc = 0

            if mid_x < (640 / 2 - x_delta) or mid_x > (640 / 2 + x_delta):
                turn = int(arduino_map((mid_x - (640 / 2 + x_delta)), -640 / 2 + x_delta, 640 / 2 - x_delta, -75, 75))

            if mid_y < (480 / 2 - y_delta) or mid_y > (480 / 2 + y_delta):
                acc = int(arduino_map((mid_y - (480 / 2 + y_delta)), -480 / 2 + y_delta, 480 / 2 - y_delta, -75, 75))

            string = str(acc) + "," + str(turn) + ",350\n"

            cur_time = time.time()

            if prev_time == 0:
                prev_time = cur_time

            print("Time: " + str(cur_time - prev_time))
            prev_time = cur_time

            # ser.write(string.encode('utf-8'))
            print(face_names[0], face_locations[0])
            print(string)

        else:
            string = str(0) + "," + str(0) + ",350\n"
            #ser.write(string.encode('utf-8'))
            
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
