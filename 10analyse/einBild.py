import logging
import cv2
import matplotlib.pyplot as plt


def analysieren(db, pfad):
    logging.debug(f"Analysiere Bild: {pfad}")

    img = cv2.imread(pfad)
    cv2.imshow("guiBild", img)
    k = cv2.waitKey(100000)

    return k != 27
