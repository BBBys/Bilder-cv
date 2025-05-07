#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  P0sammeln.py
#    Bildverarbeitung © 2025 by Burkhard Borys is licensed under CC BY-NC-SA 4.0 
#    https://creativecommons.org/licenses/by-nc-sa/4.0/
#    This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
import mysql.connector
import logging,argparse
from erfassen import erfassen
from dbroutinen import dbcreate,pfadEintragen
from dbparam import *
#from pprint import pprint
from datetime import date,datetime,timedelta
#from RSSLesen import rsslesen
TITEL='P0Sammeln'
VERSION='V0'
VERARBEITEN='verarbeiten!'
            
def EinträgeWiederherstellen(db):
    """stellt fehlende Aufträge wieder her

    Raises:
        Exception: endet immer mit Exception
    """
    logging.debug('kein Startrecord gefunden')
    logging.debug('Einträge wiederherstellen')
    with db.cursor() as cursor:
        SQL = f"insert into {DBTBB} (programm) values ('{TITEL}')"
        cursor.execute(SQL)
    db.commit()
    raise Exception('Tabelle %s Einträge %s erzeugt - Neustart notwendig'%(DBTBB,TITEL));
    #endet hier

def main(pfad ):
    """Hauptprogramm

    Args:
        pfad (string): Pfad mit letztem /

    Returns:
        string: Meldungen, nicht notwendig
    """
    try:
        mydb =mysql.connector.connect(host=DBHOST,db=DBNAME,user = DBUSER, port = DBPORT, password = DBPWD)  #+ ";ConvertZeroDateTime=True;", 
        if pfad != VERARBEITEN:return pfadEintragen(mydb,TITEL,pfad)
        
        with mydb.cursor() as mycursor:
            SQL = "SELECT id,parameter FROM %s WHERE programm='%s';"%(DBTBB,TITEL)
            mycursor.execute(SQL) 
            Aufträge=mycursor.fetchall()
        logging.debug('%d Records'%len(Aufträge))

        if len(Aufträge)<1:
            return 'kein Auftrag vorhanden'
        #es gibt indestens 1 Aufträge
            
        Auftrag=Aufträge[0]    # nur den ersten
        logging.debug(Auftrag)
        id=Auftrag[0]
        pfad=Auftrag[1]
        logging.info(f"{TITEL}: Start Auftrag {pfad}")
        ok=erfassen(pfad,mydb,TITEL)
        if ok:
            with mydb.cursor() as mycursor:
                SQL = f"DELETE FROM {DBTBB} WHERE id={id};"
                mycursor.execute(SQL) 
                mydb.commit()     
            logging.info(f"{TITEL}: Auftrag {Auftrag[0]} erfolgreich")
        else:
            logging.error(f"{TITEL}: Auftrag {Auftrag[0]} nicht erfolgreich")
        
    except mysql.connector.errors.ProgrammingError as e:
        logging.error(e)
        match e.errno:
            case 1064: 
                print("Syntax Error: {}".format(e))
            case 1146: 
                dbcreate(mydb,e.msg)
            case _:
                logging.fatal(e)
    except Exception as e:
        logging.fatal(e)
    finally:
        mydb.close()
    return 0

if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(
                    prog=TITEL,
                    description='Bilder suchen und in DB schreiben')    
    parser.add_argument('pfad',nargs='?',default=VERARBEITEN,
                        help="optional: Pfad in DB, dann keine Verarbeitung")
    parser.add_argument("-v", "--verbose", dest="pVerbose", action='store_true', help="Debug-Ausgabe")
    arguments = parser.parse_args()
    pfad=arguments.pfad
    Dbg= arguments.pVerbose
    if Dbg:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info('Start %s: %s'%(TITEL,pfad))
    
    sys.exit(main(pfad))
