import mysql.connector
from dbroutinen import pfadEintragen
from dbparam import *
import logging, os


def erfassen(ausgangspfad, db, titel):
    logging.debug(f"erfassen:{ausgangspfad} Start...")
    exts = [".jpg", ".jpeg", ".png", ".CR2", ".cr2", ".JPG", ".JPEG", ".PNG"]
    with db.cursor() as cursor:
        for pfad, dirs, files in os.walk(ausgangspfad):
            # logging.debug('erfassen:root %s',root)
            # logging.debug('erfassen:dirs= %s',dirs)
            logging.debug("erfassen:files %s", files)
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext in exts:
                    logging.debug(
                        f"bearbeiten:erfassen:{pfad}, {name}, {ext}"
                    )
                    sql = f"INSERT INTO {DBTBILDER} (pfad,name,ext) VALUES ('{pfad}', '{name}', '{ext}');"
                    cursor.execute(sql)
            for dir in dirs:
                logging.debug(f"eintragen:{pfad}, {dir}")
                pfadEintragen(db, titel, os.path.join(pfad, dir))
            break
    db.commit()
    return True
