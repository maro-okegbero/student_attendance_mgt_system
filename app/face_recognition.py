import cv2

import face_recognition


def compare(pic_first, pic_second):
    """

    :param pic_first:
    :param pic_second:
    :return:
    """
    # first step : convert the images from RGB to BGR
    # This is because the face-recognition app uses opencv and opencv uses BGR
    first_pic = face_recognition.load_image_file(pic_first)
    first_pic = cv2.cvtColor(first_pic, cv2.COLOR_BGR2RGB)

    second_pic = face_recognition.load_image_file(pic_second)
    print(second_pic, "imageTest")
    second_pic = cv2.cvtColor(second_pic, cv2.COLOR_BGR2RGB)
    print(second_pic, "imageTest")

    # second step: Locate the faces in the image
    print(face_recognition.face_locations(first_pic))
    face_location = face_recognition.face_locations(first_pic)[0]
    first_picture_encoded = face_recognition.face_encodings(first_pic)[0]
    cv2.rectangle(first_pic, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (255, 2, 252), 2)

    face_location = face_recognition.face_locations(second_pic)[0]
    second_picture_encoded = face_recognition.face_encodings(second_pic)[0]
    cv2.rectangle(second_pic, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (255, 2, 252), 2)

    # third step: compare the faces in the
    results = face_recognition.compare_faces([first_picture_encoded], second_picture_encoded, tolerance=0.4)
    distance = face_recognition.face_distance([first_picture_encoded], second_picture_encoded)

    print(results, distance)
    # cv2.imshow('Maro', first_pic)
    # cv2.imshow('Maro_test', second_pic)
    #
    # cv2.waitKey(0)
    return results[0]

