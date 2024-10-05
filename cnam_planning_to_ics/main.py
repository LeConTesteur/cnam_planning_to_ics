import sys
import argparse
import csv
from io import IOBase
from typing import List, Optional
from pathlib import Path
from collections import namedtuple
from pydantic import BaseModel
from datetime import datetime, timezone

from ics import Calendar, Event, Organizer, Attendee


IN_ENCODING='iso-8859-1'
UTF_ENCODING='utf-8'
planning_csv_type=argparse.FileType('r', encoding=IN_ENCODING)
ics_type=argparse.FileType('w', encoding=UTF_ENCODING)

Ligne = namedtuple('Ligne',
    [
        'objet',
        'debut_journee',
        'debut_heure',
        'fin_journee',
        'fin_heure',
        'journee_entiere',
        'rappel',
        'date_rappel',
        'heure_rappel',
        "organisateur",
        'participants_obligatoires',
        'participants_facultatifs',
        'ressources',
        'disponibilite',
        'categories',
        'diffusion',
        'description',
        'emplacement',
        'facturation',
        'kilometrage',
        'priorite',
        'prive'
    ]
)

def to_date(journee: str, heure: str):
    return datetime.strptime(f'{journee} {heure} CEST+0200', '%d/%m/%Y %H:%M:%S %Z%z')

def to_bool(value: str) -> bool:
    return value == 'Vrai'

class LigneInfo(BaseModel):
    objet: str
    debut: datetime
    fin: datetime
    journee_entiere: bool
    rappel: Optional[datetime]
    organisateur: str
    participants_obligatoires: str
    participants_facultatifs: str
    ressource: str
    disponiblite: str
    categories: str
    diffusion: str
    description: str
    emplacement: str
    facturation: str
    kilometrage: str
    priorite: str
    prive: bool
    
    @staticmethod
    def from_ligne(ligne:Ligne):
        return LigneInfo(
            objet=ligne.objet,
            debut=to_date(ligne.debut_journee, ligne.debut_heure),
            fin=to_date(ligne.fin_journee, ligne.fin_heure),
            journee_entiere=to_bool(ligne.journee_entiere),
            rappel=to_date(ligne.date_rappel, ligne.heure_rappel) if to_bool(ligne.rappel) else None,
            organisateur=ligne.organisateur,
            participants_obligatoires=ligne.participants_obligatoires,
            participants_facultatifs=ligne.participants_facultatifs,
            ressource=ligne.ressources,
            disponiblite=ligne.ressources,
            categories=ligne.categories,
            diffusion=ligne.diffusion,
            description=ligne.description,
            emplacement=ligne.emplacement,
            facturation=ligne.facturation,
            kilometrage=ligne.kilometrage,
            priorite=ligne.priorite,
            prive=to_bool(ligne.prive)
        )
    
    def to_event(self) -> Event:
        return Event(
            name=self.objet, 
            begin=self.debut,
            end=self.fin, 
            description=self.description,
            location=self.emplacement,
            transparent=self.prive,
            attendees=[Attendee(self.participants_obligatoires)], # TODO participant facultatif
            organizer=Organizer(self.organisateur)
        )

def ligne_to_event(ligne: List[str]) -> Event:
    return LigneInfo.from_ligne(Ligne(*ligne)).to_event()

def remove_header(reader):
    next(reader)

def parse_csv(fd: IOBase) -> List[Event]:
    reader = csv.reader(fd, delimiter=',', quotechar='"')
    remove_header(reader)
    return [
        ligne_to_event(ligne)
        for ligne in reader
    ]

def main(argv):
    parser = argparse.ArgumentParser(argv[0])
    parser.add_argument('planning_csv', type=planning_csv_type, help='Le planning au format csv')
    parser.add_argument('--ics', required=True, type=ics_type, help='Le fichier ics généré')
    args = parser.parse_args(argv[1:])
    
   
    event_list = parse_csv(args.planning_csv)

    c = Calendar()
    for e in event_list:
        c.events.add(e)
    args.ics.writelines(c.serialize_iter())

if __name__ == "__main__":
    main(sys.argv)