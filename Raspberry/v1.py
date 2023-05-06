import cv2
import numpy as np
import face_recognition
from typing import List
import traceback

class Distance():

    def __init__(self, real_distance, real_width):
        ref_image = face_recognition.load_image_file('ref_image.jpg')
        ref_image_location = face_recognition.face_locations(ref_image)[0]
        ref_image_height, ref_image_width = ref_image.shape[:2]
        print("Dimensione immagine (HxW): " + str(ref_image_height) + "x" + str(ref_image_width))

        self.ref_width = ref_image_width-ref_image_location[1]-ref_image_location[3] # image_width - right - left

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
        for (top, right, bottom, left) in bounding_boxes:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            obj_width = 640 - right - left

            if obj_width != 0:
                distances.append(self._calc_distance(Focal_length, self.real_width, obj_width))
            else:
                distances.append(0)

        return distances

if __name__ == '__main__':
    dist = Distance(real_distance = 48, real_width = 16)
    #detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    try:
    
        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("resources/obama.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("resources/biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Load a third sample picture and learn how to recognize it.
        davide_image = face_recognition.load_image_file("resources/davide.jpeg")
        davide_face_encoding = face_recognition.face_encodings(davide_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding,
            davide_face_encoding
        ]
        known_face_names = [
            "Barack Obama",
            "Joe Biden",
            "Davide"
        ]

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        #debug
        video_capture_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        video_capture_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Dimensione video_capture (HxW): " + str(video_capture_height) + "x" + str(video_capture_width))
    except:
        traceback.print_exc()

    while(True):

        try:
            # Grab a single frame of video
            ret, frame = video_capture.read()

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

                    # If a match was found in known_face_encodings use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            distances = dist.get_distances(bounding_boxes=face_locations)

            #Display the result
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

                cv2.putText(frame, "Distance: {:.2f}".format(distances[idx]), (left + 35, bottom- 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 1255), 2)
        except:
            traceback.print_exc()
            
        cv2.imshow("frame", frame)
                
        if cv2.waitKey(1) == ord('q'):
            break
            
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
