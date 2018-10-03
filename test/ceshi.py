import face_recognition
import base64

img_open = open('obama.jpg', 'rb')

img_open_fuben = open('obama_fuben.jpg', 'wb')
img_open_fuben.write(img_open.read())

img_load = face_recognition.load_image_file('obama.jpg')

# print(img_open.read())
# print(img_load)



img_open.close()
img_open_fuben.close()
