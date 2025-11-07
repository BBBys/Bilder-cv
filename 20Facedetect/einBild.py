import logging
import os
import cv2

# from scipy.misc import lena
# import matplotlib.pyplot as plt
# import numpy as np


def faceDetect(einpfad, name, ext, face_cascade):

    eindatei = os.path.join(einpfad, name + ext)
    logging.debug(f"Analysiere Bild: {eindatei}")
    img = cv2.imread(eindatei)

    # img = lena().astype(np.uint8)
    for x, y, w, h in face_cascade.detectMultiScale(img, 1.3, 5):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    warten = 300
    cv2.imshow("Bild", img)
    k = cv2.waitKey(333 * warten)

    return k != 27
