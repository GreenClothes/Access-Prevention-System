from person_db import Person
from person_db import Face
from person_db import PersonDB
import face_recognition
import numpy as np
from datetime import datetime
import cv2

detect_past = set()
exit_flg = False
detect_num = 0
detect_flg = False
detect_img = []

class FaceClassifier():
    def __init__(self, threshold, ratio):
        self.similarity_threshold = threshold
        self.ratio = ratio

    def get_face_image(self, img_frame, box):
        img_height, img_width = img_frame.shape[:2]
        (box_top, box_right, box_bottom, box_left) = box
        box_width = box_right - box_left
        box_height = box_bottom - box_top
        crop_top = max(box_top - box_height, 0)
        pad_top = -min(box_top - box_height, 0)
        crop_bottom = min(box_bottom + box_height, img_height - 1)
        pad_bottom = max(box_bottom + box_height - img_height, 0)
        crop_left = max(box_left - box_width, 0)
        pad_left = -min(box_left - box_width, 0)
        crop_right = min(box_right + box_width, img_width - 1)
        pad_right = max(box_right + box_width - img_width, 0)
        face_image = img_frame[crop_top:crop_bottom, crop_left:crop_right]
        if (pad_top == 0 and pad_bottom == 0):
            if (pad_left == 0 and pad_right == 0):
                return face_image
        padded = cv2.copyMakeBorder(face_image, pad_top, pad_bottom,
                                    pad_left, pad_right, cv2.BORDER_CONSTANT)
        return padded

    # return list of dlib.rectangle
    def locate_faces(self, locate_frame):
        if self.ratio == 1.0:
            # rgb = locate_frame[:, :, ::-1]
            rgb = cv2.cvtColor(locate_frame, cv2.COLOR_BGR2RGB)
        else:
            small_frame = cv2.resize(locate_frame, (0, 0), fx=self.ratio, fy=self.ratio)
            # rgb = small_frame[:, :, ::-1]
            rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        try:
            boxes = face_recognition.face_locations(rgb)
        except Exception as e:
            print('ERROR OCCUR', e)
        if self.ratio == 1.0:
            return boxes
        else:
            return []

    def compare_with_known_persons(self, face, persons):
        if len(persons) == 0:
            return False

        # see if the face is a match for the faces of known person
        encodings = [p.encoding for p in persons]
        distances = face_recognition.face_distance(encodings, face.encoding)
        index = np.argmin(distances)
        min_value = distances[index]
        if min_value < self.similarity_threshold:
            # face of known person
            persons[index].add_face(face)
            # re-calculate encoding
            persons[index].calculate_average_encoding()
            face.name = persons[index].name
            return persons[index]

    def detect_faces(self, face_frame):
        boxes = self.locate_faces(face_frame)
        if len(boxes) == 0:
            return []
        # faces found
        faces = []
        now = datetime.now()
        str_ms = now.strftime('%Y%m%d_%H%M%S.%f')[:-3] + '-'
        encodings = face_recognition.face_encodings(face_frame, boxes)
        print('82')
        for i, box in enumerate(boxes):
            face_image = self.get_face_image(face_frame, box)

            face = Face(str_ms + str(i) + ".png", face_image, encodings[i])
            face.location = box
            faces.append(face)
        return faces

def run(frame, pdb):
    threshold = 0.44
    resize_ratio = 1.0

    detect_names = []
    detect_faces = []

    ratio = float(resize_ratio)

    fc = FaceClassifier(threshold, ratio)
    print('detecting....')
    # this is core
    try:
        faces = fc.detect_faces(frame)
        for face in faces:
            person = fc.compare_with_known_persons(face, pdb.persons)
            if person:
                # print('detect', end=' ')
                # print(person.name)
                detect_names.append(person.name)
                detect_faces.append(frame)
                continue
    except Exception as e:
        print('ERROR OCCUR', e)
    # if not faces:
    #     print('Faces are not detected!!!')
    print(len(detect_names), len(detect_faces))

    return frame, detect_names, detect_faces


if __name__ == "__main__":
    person = PersonDB()
    person.load_db('students')

    src = cv2.VideoCapture(0)
    while 1:
        ret, frame = src.read()
        run(frame, person)
