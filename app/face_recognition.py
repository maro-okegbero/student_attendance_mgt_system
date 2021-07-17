import cv2
import numpy as np
import face_recognition


def compare(pic_first, pic_second):
    """

    :param pic_first:
    :param pic_second:
    :return:
    """
    # first step : convert the images from RGB to BGR
    # This is because the face-recognition app uses opencv and opencv uses BGR
    imgMaro = face_recognition.load_image_file(pic_first)
    imgMaro = cv2.cvtColor(imgMaro, cv2.COLOR_BGR2RGB)

    imgTest = face_recognition.load_image_file(pic_second)
    print(imgTest, "imageTest")
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)
    print(imgTest, "imageTest")

    # second step: Locate the faces in the image
    print(face_recognition.face_locations(imgMaro))
    faceLoc = face_recognition.face_locations(imgMaro)[0]
    encodeMaro = face_recognition.face_encodings(imgMaro)[0]
    cv2.rectangle(imgMaro, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 2, 252), 2)

    faceLoc = face_recognition.face_locations(imgTest)[0]
    encodeTest = face_recognition.face_encodings(imgTest)[0]
    cv2.rectangle(imgTest, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 2, 252), 2)

    # third step: compare the faces in the
    results = face_recognition.compare_faces([encodeMaro], encodeTest)
    distance = face_recognition.face_distance([encodeMaro], encodeTest)

    print(results, distance)
    # cv2.imshow('Maro', imgMaro)
    # cv2.imshow('Maro_test', imgTest)
    #
    # cv2.waitKey(0)
    return results[0]

