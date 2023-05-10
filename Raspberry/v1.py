import cv2
import numpy as np
import face_recognition
import serial
from typing import List
import time

def arduino_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

x_delta = 50
y_delta = 45

class Distance():

    def __init__(self, real_distance, real_width):
        ref_image = face_recognition.load_image_file('ref_image.jpg')
        ref_image_location = face_recognition.face_locations(ref_image)[0]

        self.ref_width = ref_image_location[1]-ref_image_location[3] # right - left
        print(self.ref_width)

        self.real_distance = real_distance
        self.real_width = real_width

    def _focal_length(self, measured_dist: float, real_width: float, ref_width: int) -> float:
        focal_length = (ref_width / real_width) * measured_dist
        return focal_length

    def _calc_distance(self, focal_length: float, real_width: float, actual_width: int) -> float:
        distance = (real_width / actual_width) * focal_length
        return distance

    def get_distances(self, bounding_boxes: np.ndarray) -> List[int]:
        Focal_length = self._focal_length(self.real_distance, self.real_width, self.ref_width)

        distances = list()
        for (_, right, _, left) in bounding_boxes:
            obj_width = 4*right - 4*left  # resize *4
            print(obj_width)

            if obj_width != 0:
                distances.append(self._calc_distance(Focal_length, self.real_width, obj_width))
            else:
                distances.append(0)

        return distances

if __name__ == '__main__':
    dist = Distance(real_distance = 48, real_width = 16)

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    
    # Load a sample picture and learn how to recognize it.
   # obama_image = face_recognition.load_image_file("../resources/obama.jpg")
   # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
   # biden_image = face_recognition.load_image_file("../resources/biden.jpg")
   # biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Load a third sample picture and learn how to recognize it.
    davide_image = face_recognition.load_image_file("ref_image.jpg")
    davide_face_encoding = face_recognition.face_encodings(davide_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        #obama_face_encoding,
        #biden_face_encoding,
        davide_face_encoding
    ]
    known_face_names = [
        #"Barack Obama",
        #"Joe Biden",
        "Davide"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    prev_time=0

    while(True):
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 0)

        # Only process every other frame of video to save time
        if process_this_frame and ret:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                   first_match_index = matches.index(True)
                   name = known_face_names[first_match_index]

                # Or instead use the known face with the smallest distance to the new face
                # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #    name = known_face_names[best_match_index]

                face_names.append(name)

        #process_this_frame = not process_this_frame

        #distances = dist.get_distances(bounding_boxes=face_locations)

        #print(face_names)

        if len(face_names) > 0 and face_names[0] != 'Unknown':
            # id = names[id]
            #mid_x = x + w / 2
            #mid_y = y + h / 2

            mid_x = 4*face_locations[0][3] + (4*face_locations[0][1] - 4*face_locations[0][3])/2  # resize *4, left + (right - left)/2
            mid_y = 4*face_locations[0][0] + (4*face_locations[0][2] - 4*face_locations[0][0])/2  # resize *4, top + (bottom - top)/2
            print(mid_x, mid_y)

            turn = 0
            acc = 0

            if mid_x < (640 / 2 - x_delta) or mid_x > (640 / 2 + x_delta):
                turn = int(arduino_map((mid_x - (640 / 2 + x_delta)), -640 / 2 + x_delta, 640 / 2 - x_delta, -75, 75))

            if mid_y < (480 / 2 - y_delta) or mid_y > (480 / 2 + y_delta):
                acc = int(arduino_map((mid_y - (480 / 2 + y_delta)), -480 / 2 + y_delta, 480 / 2 - y_delta, -75, 75))

            string = str(acc) + "," + str(turn) + ",350\n"

            cur_time = time.time()
            if prev_time == 0:
                prev_time= cur_time
            ser.write(string.encode('utf-8'))
            #print(face_names[0], face_locations[0])
            print("Time: "+ str(cur_time-prev_time))
            print(string)
            prev_time = cur_time
        
        else:
            string = str(0) + "," + str(0) + ",350\n"
            ser.write(string.encode('utf-8'))

        #Display the result
        '''
        for idx, ((top, right, bottom, left), name) in enumerate(zip(face_locations, face_names)):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, face_names[idx], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.putText(frame, "Distance: {:.2f}".format(distances[idx]), (left - 15, bottom+10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 1255), 2)
            
        cv2.imshow("frame", frame)
        '''

        if cv2.waitKey(1) == ord('q'):
            break
            
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
