from google.cloud import firestore
from datetime import datetime, timedelta
import time

db = firestore.Client()
collection_time = 120  # Tempo per aggiornare la collezione in minuti


def get_data_from_firebase():
    collection_name = 'PostScheduled'

    try:
        current_time = datetime.now().replace(second=0, microsecond=0)
        end_time = current_time + timedelta(minutes=collection_time)

        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        print(f"Data e ora attuale: {current_time_str}")
        print(f"Data e ora +tempo: {end_time_str}")

        collection_ref = db.collection(collection_name).where(
            'data', '>=', current_time_str
        ).where(
            'data', '<', end_time_str
        )

        docs = collection_ref.get()
        data = []

        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id  # Aggiungo l'ID del documento ai dati
            data.append(doc_data)
            print(f"Documento recuperato: {doc_data}")
        return data
    except Exception as e:
        print(f"Errore nel recupero dei dati: {e}")
        return []


# Funzione per verificare se c'è una corrispondenza tra l'orario attuale e i dati recuperati
def check_for_matching_time(data):
    current_time_str = datetime.now().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    to_remove = []  # Lista di elementi da rimuovere dopo la corrispondenza

    for entry in data:
        event_time_str = entry['data']
        if current_time_str == event_time_str:
            print(f"Evento trovato con ID {entry['id']} alle {event_time_str}")
            socials = entry['social']
            for social in socials:
                print(f'Creato il post per il social: {social}')
            to_remove.append(entry)  # Aggiungi l'elemento alla lista per rimuoverlo

    # Rimuovi gli eventi trovati dalla lista principale
    for entry in to_remove:
        data.remove(entry)
        print(f"Evento con ID {entry['id']} rimosso dalla lista")


def on_snapshot(col_snapshot, changes, read_time):
    print(f'Notifica di cambiamenti da Firestore al {read_time}:')
    for change in changes:
        if change.type.name == 'ADDED':
            print(f"Nuovo documento aggiunto: {change.document.id}")
            # Esegui operazioni sui nuovi documenti
            check_for_matching_time([change.document.to_dict()])
        elif change.type.name == 'MODIFIED':
            print(f"Documento modificato: {change.document.id}")
            # Gestisci le modifiche sui documenti
            check_for_matching_time([change.document.to_dict()])
        elif change.type.name == 'REMOVED':
            print(f"Documento rimosso: {change.document.id}")
            # Gestisci la rimozione dei documenti se necessario


# Imposta il listener per i cambiamenti sulla collezione PostScheduled
def setup_firestore_listener():
    print("Impostazione listener per Firestore...")
    collection_name = 'PostScheduled'  # Cambia con il nome reale della collection
    collection_ref = db.collection(collection_name)

    # Aggiungi un listener per la collection
    collection_ref.on_snapshot(on_snapshot)


# Funzione principale che inizializza i dati e imposta il listener
def main():
    data = get_data_from_firebase()  # Recupero iniziale dei dati
    check_for_matching_time(data)  # Verifica se ci sono corrispondenze iniziali
    setup_firestore_listener()  # Imposta il listener in tempo reale
 
    # Mantiene il programma attivo per permettere al listener di funzionare
    while True:
        time.sleep(1)  # Mantiene il ciclo vivo, puoi eseguire altre operazioni qui


# Avvio della funzione principale
if __name__ == "__main__":
    main()
