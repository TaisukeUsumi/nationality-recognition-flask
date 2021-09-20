import cv2
import numpy as np
from keras.models import load_model


class Prediction:
    @staticmethod
    def predict(image_path):
        image = cv2.imread(image_path)

        image_size = 128

        face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_model.xml')
        face = face_cascade.detectMultiScale(image)[0]
        x, y, w, h = face
        image = image[y:y + h, x:x + w]
        facial_image = cv2.resize(image,
                                (image_size, image_size))
        facial_image = np.reshape(
            facial_image, (1, image_size, image_size, 3))

        model = load_model('./model/nationality_recognition_model.h5')
        result = model.predict(facial_image)[0]

        nationality_result = np.argmax(result)

        if nationality_result == 0:
            nationality = 'Chinese'
        elif nationality_result == 1:
            nationality = 'Japanese'
        else:
            nationality = 'Korean'

        chinese_probability = round(result[0]*100)
        japanese_probability = round(result[1]*100)
        korean_probability = 100 - chinese_probability - japanese_probability

        probability_list = [str(chinese_probability) + "%",
                            str(japanese_probability) + "%",
                            str(korean_probability) + "%"]

        return nationality, probability_list
