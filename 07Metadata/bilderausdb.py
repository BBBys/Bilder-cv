from dbparam import DBTBILDER
import logging, pprint
from einBild import metasuche


def safeadd(setobj, value):
    if value not in setobj:
        setobj.add(value)


def bilderAusDB(db, titel):
    kameras = {"leer"}
    kameras.clear()
    fotografenundkameras = {"leer"}
    fotografenundkameras.clear()
    fotografen = {"leer"}
    fotografen.clear()
    logging.debug(f"analysieren Start...")
    exts = [".jpg", ".jpeg", ".png", ".CR2", ".cr2", ".JPG", ".JPEG", ".PNG"]
    with db.cursor(dictionary=True, buffered=True) as curEin:
        sql = f"SELECT id,pfad,name,ext FROM {DBTBILDER} ;"
        curEin.execute(sql)
        bilder = curEin.fetchall()
    n = 0
    for bild in bilder:
        einekamera = einfotograf = None
        einpfad = bild["pfad"]
        name = bild["name"]
        ext = bild["ext"]
        id = bild["id"]
        if ext not in exts:
            continue
        ergebnis = metasuche(einpfad, name, ext)
        n += 1
        for key, value in ergebnis.items():
            match key:
                case "kamera":
                    einekamera = value
                    safeadd(kameras, value)
                case "fotograf":
                    einfotograf = value
                    safeadd(fotografen, value)
                case _:
                    print(f"XXneuXX  {key}: {value}")
            if einekamera and einfotograf:
                logging.warning(f"Bild {name}")
                logging.warning(f"Kamera {einekamera}")
                logging.warning(f"Fotograf {einfotograf}")
                safeadd(fotografenundkameras, f"{einfotograf} mit {einekamera}")
                # with db.cursor(dictionary=True, buffered=True) as curEin:
            #    sql = f"UPDATE {DBTBILDER} SET arbkopie ='{auspfad}' WHERE id={id};"
            #    curEin.execute(sql)
            # if not weiter:
            #    break
            print(f"{titel}: {n}. Bild ID:{id} {name}{ext} analysiert.")
            print("----------------------------------------------")
    print("--------------------------------")
    print("Kameras:")
    i = 1
    for k in kameras:
        print(f"{i}. {k}")
        i += 1
    print("--------------------------------")
    print("Fotografen:")
    i = 1
    for f in fotografen:
        print(f"{i}. {f}")
        i += 1
    print("--------------------------------")
    print("Fotografen mit Kamera:")
    i = 1
    for fk in fotografenundkameras:
        print(f"{i}. {fk}")
        i += 1
    # db.commit()
    return True
