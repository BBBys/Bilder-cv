import logging
import cv2, os


def breiteSetzen(einpfad, name, ext, auspfad, ziel):
    eindatei = os.path.join(einpfad, name + ext)
    logging.debug(f"Analysiere Bild: {eindatei}")
    img = cv2.imread(eindatei)
    logging.debug(f"Original Bildgröße: {img.shape}")
    h, w = img.shape[:2]
    maxhw = max(h, w)
    resize = maxhw > ziel
    if resize:
        logging.debug("Bild wird verkleinert")
        fakt = ziel / maxhw
        img = cv2.resize(img, None, fx=fakt, fy=fakt)
    else:
        logging.debug("Bild kleiner als Zielbreite, kein Ändern")
    if auspfad is not None:
        ausdatei = os.path.join(auspfad, name + ext)
        logging.debug(f"Speichere Bild: {ausdatei}")
        match ext.lower():
            case ".jpg" | ".jpeg":
                rtn = cv2.imwrite(ausdatei, img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            case ".png":
                rtn = cv2.imwrite(ausdatei, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            case _:
                logging.exception(f"Unbekannte Dateierweiterung: {ext}")
        if rtn:
            warten = 1
        else:
            logging.warning(f"Speichern {ausdatei}")
            warten = 300
    cv2.imshow("Bild", img)
    k = cv2.waitKey(333 * warten)

    return k != 27
