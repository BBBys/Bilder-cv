#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Metad.py
#
#    Fotos analysieren - Metadaten auslesen und in DB speichern
# (c) 2025 by Bernd-Burkhard Borys
# licensed under CC BY-NC-SA 4.0.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate
from dbparam import *
from bilderausdb import bilderAusDB

TITEL = "P07Metadata"
VERSION = "V0"


def main():
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, password=DBPWD
        )

        logging.info(f"{TITEL}: Start Analyse")
        ok = bilderAusDB(mydb, TITEL)
        if ok:
            logging.info(f"{TITEL}: Metadaten-Suche erfolgreich")
        else:
            logging.error(f"{TITEL}: Metadatensuche nicht erfolgreich")

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
    parser = argparse.ArgumentParser(prog=TITEL, description="Metadaten suchen ")
    # parser.add_argument("aus", help="Verzeichnis Bilderausgabe", nargs="?", default=None)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="pVerbose",
        action="store_true",
        help="Debug-Ausgabe",
        default=False,
    )

    arguments = parser.parse_args()
    if arguments.pVerbose:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info(f"Start {TITEL}")

    sys.exit(main())
