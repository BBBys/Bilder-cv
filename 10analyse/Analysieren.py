#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Analysieren.py
#
#    Fotos analysieren  
# (c) 2025 by Bernd-Burkhard Borys
# licensed under CC BY-NC-SA 4.0.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

import mysql.connector
import logging, argparse
from dbroutinen import dbcreate,  zurücksetzenBilder
from dbparam import *
from datetime import date, datetime, timedelta

TITEL = "P10Analysieren"
VERSION = "V0"

def main():
    """Hauptprogramm

    Args:

    Returns:
        string: Meldungen, nicht notwendig
    """
    try:
        mydb = mysql.connector.connect(
            host=DBHOST, db=DBNAME, user=DBUSER, port=DBPORT, \
                password=DBPWD       )  # + ";ConvertZeroDateTime=True;",
        if ZURÜCK:
            # Code zum Zurücksetzen
            logging.info("Zurücksetzen")
            #zurücksetzenBilder(TITEL, mydb)
            logging.info("...zurückgesetzt, Ende")
            return 0

        
        logging.info(f"{TITEL}: Start Analyse")
        ok = analysieren(mydb, TITEL)
        if ok:
            logging.info(f"{TITEL}: Analyse erfolgreich")
        else:
            logging.error(f"{TITEL}: Analyse nicht erfolgreich")

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

    #LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
    LOG_FORMAT = "%(name)s %(levelname)s %(message)s"
    parser = argparse.ArgumentParser(
        prog=TITEL, description="Bilder analysieren "
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="pVerbose",
        action="store_true",
        help="Debug-Ausgabe",
    )
    parser.add_argument(
        "-z",
        "--zurücksetzen",
        dest="pZurck",
        action="store_true",
        help="alle Analyseergebnisse löschen",
    )
    arguments = parser.parse_args()
    ZURÜCK = arguments.pZurck
    Dbg = arguments.pVerbose
    if Dbg:        LOG_LEVEL = logging.DEBUG
    else:          LOG_LVEL = logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info("Start %s" % (TITEL))

    sys.exit(main())
