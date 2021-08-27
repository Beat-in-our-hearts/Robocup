import cv2 as cv

src = cv.imread('../example/example1.png')
cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
cv.rectangle(src, (763, 509), (763+155, 509+162), (0, 0, 255))
cv.imshow('input_image', src)
cv.waitKey(0)
cv.destroyAllWindows()
# [{'face_token': '4eace182661b8b496775d6f72712a454', 'location': {'left': 763.09, 'top': 509.42, 'width': 155, 'height': 162, 'rotation': 0}, 'face_probability': 1, 'angle': {'yaw': -1.37, 'pitch': 17.99, 'roll': -1.83}, 'age': 49, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': '706112df01f10fd855a29b70408f05b7', 'location': {'left': 1022.58, 'top': 107.31, 'width': 132, 'height': 145, 'rotation': 4}, 'face_probability': 1, 'angle': {'yaw': 7.23, 'pitch': -10.57, 'roll': 7.46}, 'age': 29, 'expression': {'type': 'none', 'probability': 0.68}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': 'd0033a08e4766e6026a8e878160e1eb3', 'location': {'left': 62.99, 'top': 460.63, 'width': 142, 'height': 129, 'rotation': 15}, 'face_probability': 1, 'angle': {'yaw': -31.16, 'pitch': -4.73, 'roll': 11.43}, 'age': 30, 'expression': {'type': 'smile', 'probability': 0.54}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': 'd6c3b029057446a46703d5726696409f', 'location': {'left': 535.88, 'top': 462.34, 'width': 136, 'height': 130, 'rotation': 5}, 'face_probability': 1, 'angle': {'yaw': -25.31, 'pitch': -15.89, 'roll': -1.12}, 'age': 31, 'expression': {'type': 'none', 'probability': 0.82}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': '63b826c586b1ec5ce0a6640c5e164479', 'location': {'left': 63.66, 'top': 101.17, 'width': 127, 'height': 135, 'rotation': 0}, 'face_probability': 1, 'angle': {'yaw': -10.64, 'pitch': -6.82, 'roll': -3.81}, 'age': 33, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': 'a598ee072f7eee9812cd5a88541a146a', 'location': {'left': 297.39, 'top': 531.73, 'width': 126, 'height': 136, 'rotation': -7}, 'face_probability': 1, 'angle': {'yaw': 7.01, 'pitch': 10.96, 'roll': -10.89}, 'age': 40, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': 'eb1a306832042470cee14a564ffb2c29', 'location': {'left': 530.74, 'top': 110.1, 'width': 125, 'height': 123, 'rotation': 4}, 'face_probability': 1, 'angle': {'yaw': 0.04, 'pitch': 5.65, 'roll': 2.9}, 'age': 36, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': '56ee417e3ea2e4b454cffeddb2d2f854', 'location': {'left': 763.97, 'top': 114.57, 'width': 121, 'height': 119, 'rotation': -6}, 'face_probability': 1, 'angle': {'yaw': 14.81, 'pitch': 8.51, 'roll': -6.89}, 'age': 35, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': '4da35889f6e62685f710dce49e6cf562', 'location': {'left': 1013.11, 'top': 505.45, 'width': 124, 'height': 112, 'rotation': 0}, 'face_probability': 1, 'angle': {'yaw': 6, 'pitch': 19.93, 'roll': -4.22}, 'age': 32, 'expression': {'type': 'smile', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}},
# {'face_token': '516c22af3874acca7fc2d3d3cc105c1e', 'location': {'left': 294.32, 'top': 132.3, 'width': 108, 'height': 103, 'rotation': -6}, 'face_probability': 1, 'angle': {'yaw': 10.47, 'pitch': 13.06, 'roll': -9.02}, 'age': 30, 'expression': {'type': 'none', 'probability': 1}, 'gender': {'type': 'male', 'probability': 1}}]}}
