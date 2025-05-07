from dbparam import *
import mysql.connector
import logging

DBTCREATEBB = """ CREATE TABLE `blackboard` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'simpler Zähler',
 `programm` tinytext DEFAULT NULL,
 `version` tinyint(4) DEFAULT 0 COMMENT 'Programmversion, falls es Unterschiede gibt',
 `parameter` tinytext DEFAULT NULL COMMENT 'Parameter für das Programm',
 `parameter2` tinytext DEFAULT NULL COMMENT 'zusätzlicher Parameter',
 `zeit` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'wann der Eintrag erzeugt wurde',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""

DBTCREATEBILDER = """ CREATE TABLE `bilder` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'simpler Zähler',
 `pfad` tinytext DEFAULT NULL,
 `name` tinytext DEFAULT NULL,
 `ext` tinytext DEFAULT NULL,
 `version` tinyint(4) DEFAULT 0 COMMENT 'Programmversion, falls es Unterschiede gibt',
 `zeit` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'wann der Eintrag erzeugt wurde',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""

def pfadEintragen(db,titel,pfad):
    """Pfad in die Tabelle eintragen

    Args:
        db (MySQL-Connection): DB-Verbindung
        pfad (string): Pfad mit / am Ende

    Returns:
        string: Meldung
    """
    with db.cursor() as cursor:
        sql=f"INSERT INTO {DBTBB} (programm,parameter) VALUES ('{titel}','{pfad}')"
        logging.debug(sql)
        cursor.execute(sql)
    db.commit()
    return 'Pfad eingetragen'


def dbcreate(db,errtext):
    """erzeugt eine fehlende Tabelle

    Args:
        cursor (MySQL-Cursor): cursor
        tabelle (string): Tabellenname

    Raises:
        Exception: wenn Name der Tabelle nicht stimmt

    Returns:
        -: 0
    """
    tabelle=errtext.split("cv.")[1].split("'")[0]
    logging.debug(f"dbcreate: {tabelle}")
    with db.cursor() as cursor:
        match tabelle:
            case 'bilder':cursor.execute(DBTCREATEBILDER)
            case 'blackboard':cursor.execute(DBTCREATEBB)
            case _:raise Exception('Tabelle %s Erzeugung unbekannt'%(tabelle))
    logging.critical('Tabelle nicht vorhanden - erzeugt')
    return 0

def zurücksetzenDaten(titel,db,lkette):
    """Daten löschen, zurücksetzen

    Raises:
        Exception: aus falschem Programm
        Exception: nicht zurückgesetzt
    """
    if titel!='P3Worter':
        raise Exception (f"Zurücksetzen aus falschem Programm aufgerufen:{titel}")
    ja=input('Zurücksetzen? Ja:')
    if ja!='Ja':
        raise Exception (f"Zurücksetzen nicht bestätigt: {ja}")
    wMarker=f"w{lkette}"
    wTab=f"woerter{lkette}"
    wAuftr=f"P3{lkette}Worter"
    with db.cursor() as cursor:
        sql=f'truncate {wTab};'
        logging.debug(sql)
        cursor.execute(sql)
        sql=f"insert into {DBTBB} (programm) values ('{wAuftr}');"
        logging.debug(sql)
        cursor.execute(sql)
        sql=f"UPDATE `{DBTDATEN}` SET `{wMarker}`=0;"
        logging.debug(sql)
        cursor.execute(sql)
    db.commit()
    logging.info('...zurückgesetzt')


