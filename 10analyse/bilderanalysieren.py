import mysql.connector
from dbroutinen import pfadEintragen
from dbparam import *
import logging, os


def bilderAnalysieren( db, titel):
    logging.debug(f"analysieren Start...")
    exts = [".jpg", ".jpeg", ".png", ".CR2", ".cr2", ".JPG", ".JPEG", ".PNG"]
    with db.cursor() as cursor:
        pass
 
    db.commit()
    return True
