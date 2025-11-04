#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Size.py
#
#    Fotos analysieren - Größe anpassen
# (c) 2025 by Bernd-Burkhard Borys
# licensed under CC BY-NC-SA 4.0.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import *
from bilderausdb import bilderAusDB

TITEL = "P05Size"
VERSION = "V0"

def main(auspfad, zielBreite):
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )  

        logging.info(f"{TITEL}: Start Analyse")
        ok = bilderAusDB(mydb, auspfad, zielBreite, TITEL)
        if ok:
            logging.info(f"{TITEL}: Größenänderung erfolgreich")
        else:
            logging.error(f"{TITEL}: Größenänderung nicht erfolgreich")

    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e)
        match e.errno:
            case 1064:
                print("Syntax Error: {}".format(e))
            case 1146:
                dbcreate(mydb, e.msg)
            case _:
                logging.exception(e)
    except Exception as e:
        logging.exception(e)
    finally:
        mydb.close()
    return 0


if __name__ == "__main__":
    import sys

    # LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_FORMAT = "%(name)s %(levelname)s %(message)s"
    parser = argparse.ArgumentParser(prog=TITEL, description="Größe ändern ")
    parser.add_argument("aus", help="Verzeichnis Bilderausgabe", nargs="?", default=None)

    parser.add_argument("-v","--verbose",dest="pVerbose",
        action="store_true",help="Debug-Ausgabe",default=False)
    parser.add_argument("-z","--ziel",dest="zielBreite",
        default=100,type=int,help="Ziel-Breite in Pixel")

    arguments = parser.parse_args()
    zielBreite = arguments.zielBreite
    auspfad = arguments.aus
    Dbg = arguments.pVerbose
    if Dbg:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info(f"Start {TITEL} -> {auspfad} Zielbreite: {zielBreite}")

    sys.exit(main(auspfad, zielBreite))
