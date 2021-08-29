from face_api.face_run import Face_BD
from PIL import Image
from other_api.plot_lable import Draw_Box_on_single_face_PIL

image_library = ["example1.png", "example3.jpeg", "example5.jpeg"]
face_baidu = Face_BD()

for image in image_library:
    result = face_baidu.find_all_faces(image)

    print(result)
    im = Image.open(image)
    for face in result["face_list"]:
        location = [int(face['location']['left']), int(face['location']['top']),
                    int(face['location']['left']) + int(face['location']['width']),
                    int(face['location']['top'] + face['location']['height'])]
        Draw_Box_on_single_face_PIL(im, location, face["gender"]['type'])

    im.show()
