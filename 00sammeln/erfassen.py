import mysql.connector
from dbroutinen import pfadEintragen
from dbparam import *
import logging,os

def erfassen(ausgangspfad,db,titel):
    logging.debug(f'erfassen:{ausgangspfad} Start...')
    with db.cursor() as cursor:
        for pfad, dirs, files in os.walk(ausgangspfad): 
            #logging.debug('erfassen:root %s',root)
            #logging.debug('erfassen:dirs= %s',dirs)
            logging.debug('erfassen:files %s',files)
            for filename in files: 
                name, ext = os.path.splitext(filename)
                logging.debug(f'bearbeiten:erfassen:{pfad}, {name}, {ext}')
                sql=f"INSERT INTO {DBTBILDER} (pfad,name,ext) VALUES ('{pfad}', '{name}', '{ext}');"
                cursor.execute(sql)
            for dir in dirs:
                logging.debug(f'eintragen:{pfad}, {dir}')
                pfadEintragen(db,titel,os.path.join(pfad,dir)            )
            break
        return True
    
    
    
        with db.cursor() as cursor:
            data=''
            i=0
            ok=hatZeit=hatMeldung= hatTitel=False
            titel=meldung=link=AuftragQuelle=AuftragZeit=''
            for line in file:                
                teile=line.partition(PART)
                logging.debug(teile)
                key=teile[0].strip(WEG)
                val=teile[2].strip(WEG)
                match key:
                    case '-----':
                        #neuer Eintrag beginnt
                        if hatTitel:
                            ok=speichern(titel,meldung,link,cursor,AuftragQuelle,AuftragZeit)
                            if not ok:
                                logging.warning(f"Fehler bein Speichern von {titel}")
                                return False
                            hatTitel=hatLink=hatZeit=hatMeldung=False
                            link=''
                            titel=''
                    case 'title':
                        titel=val
                        hatTitel=True
                    case 'summary':
                        meldung=val
                        hatMeldung=True
                    case 'updated_parsed':
                        pass
                    case 'published_parsed':
                        pass
                    case 'link':
                        link=val
                        hatLink=True
                    case _:
                        logging.error('bearbeiten:bearbeiten:match unbekannt: Key >%s< in >%s<',key,val)
                        raise Exception(f'beim Untersuchen der RSS-Einträge\nwurde der Key {key}\nam Zeilenanfang nicht erkannt\n\nDAS VERHINDERT ALLE FOLGENDEN AUSWERTUNGEN!!')
                        return False
                        #kein commit 

            #for line
    #with cursor
    logging.debug('Datei fertig')
    db.commit()
    return True

            
        