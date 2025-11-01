from dbparam import DBTBILDER
import logging, os
from einBild import analysieren


def bilderAnalysieren(db, titel):
    logging.debug(f"analysieren Start...")
    exts = [".jpg", ".jpeg", ".png", ".CR2", ".cr2", ".JPG", ".JPEG", ".PNG"]
    with db.cursor(dictionary=True, buffered=True) as cursor:
        sql = f"SELECT id,pfad,name,ext FROM {DBTBILDER} ;"
        cursor.execute(sql)
        bilder = cursor.fetchall()
    for bild in bilder:
        ext = bild["ext"]
        if ext not in exts:
            continue
        pfad = os.path.join(bild["pfad"], bild["name"] + ext)
        logging.debug(f"analysiere Bild: {pfad}")
        if not analysieren(db, pfad):
            break

    # db.commit()
    return True
