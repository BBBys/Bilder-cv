from dbparam import DBTBILDER
import logging, os
from einBild import breiteSetzen


def bilderAusDB(db, auspfad, breite, titel):
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
        weiter = breiteSetzen(einpfad, name, ext, auspfad, breite)
        with db.cursor(dictionary=True, buffered=True) as curEin:
            sql = f"UPDATE {DBTBILDER} SET arbkopie ='{auspfad}' WHERE id={id};"
            curEin.execute(sql)
        if not weiter:
            break

    db.commit()
    return True
