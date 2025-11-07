from dbparam import DBTBILDER
import logging, os
from einBild import faceDetect
import cv2

# from scipy.misc import lena
# import matplotlib.pyplot as plt
# import numpy as np
# from IPython.display import HTML
from urllib.request import urlretrieve


def bilderAusDB(db, titel):

    dir = "~/OpenCV/haarcascades/"
    base = "https://raw.githubusercontent.com/Itseez/opencv/master/data/"
    url = base + "haarcascades/haarcascade_frontalface_default.xml"
    path = os.path.join(dir, "haarcascade_frontalface_default.xml")

    if not os.path.exists(dir):
        logging.warning(f"Pfad {dir} FEHLT")
        os.makedirs(dir)
    if not os.path.exists(path):
        logging.warning(f"Lade Haarcascade Datei von {url} nach {path}")
        urlretrieve(url, path)

    face_cascade = cv2.CascadeClassifier(path)

    logging.debug(f"analysieren Start...")
    exts = [".jpg", ".jpeg", ".png", ".CR2", ".cr2", ".JPG", ".JPEG", ".PNG"]
    with db.cursor(dictionary=True, buffered=True) as curEin:
        sql = f"SELECT id,pfad,name,ext FROM {DBTBILDER} ;"
        curEin.execute(sql)
        bilder = curEin.fetchall()
    for bild in bilder:
        einpfad = bild["pfad"]
        name = bild["name"]
        ext = bild["ext"]
        id = bild["id"]
        if ext not in exts:
            continue
        weiter = faceDetect(einpfad, name, ext, face_cascade)

        if not weiter:
            break

    db.commit()
    return True
