from google.cloud import firestore
from datetime import datetime, timedelta
import time

db = firestore.Client()
collection_time = 120  # Tempo per aggiornare la collezione in minuti
data = []


# Funzione per verificare se la data del documento è entro le prossime due ore
def is_within_next_two_hours(event_time_str):
    try:
        event_time = datetime.strptime(event_time_str, '%Y-%m-%d %H:%M:%S')

        current_time = datetime.now().replace(second=0, microsecond=0)
        end_time = current_time + timedelta(minutes=collection_time)

        # Verifico se l'evento rientra nell'intervallo di tempo
        return current_time <= event_time < end_time
    except ValueError as e:
        print(f"Errore nel parsing della data: {e}")
        return False


def check_for_matching_time(dati):
    print(f"Contenuto di 'dati' passato alla funzione: {dati}")

    current_time = datetime.now().replace(second=0, microsecond=0)
    to_remove = []

    for entry in dati:
        event_time = datetime.strptime(entry['data'], '%Y-%m-%d %H:%M:%S')

        # Aggiungo una tolleranza di +/- 1 minuto
        if current_time - timedelta(minutes=1) <= event_time <= current_time + timedelta(minutes=1):
            print(f"Evento trovato con ID {entry['id']} alle {entry['data']}")
            socials = entry['social']
            for social in socials:
                print(f'Creato il post per il social: {social}')
            to_remove.append(entry)  # Aggiungo l'elemento alla lista per rimuoverlo

    # Rimuovo gli eventi trovati dalla lista principale
    for entry in to_remove:
        try:
            data.remove(entry)
            print(f"Evento con ID {entry['id']} rimosso dalla lista globale `data`")
        except ValueError:
            print(f"Errore: L'elemento con ID {entry['id']} non è presente nella lista globale `data`")

    print(f"Stato attuale della lista `data`: {data}")


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
        global data

        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id  # Aggiungo l'ID del documento ai dati

            # Controllo se il documento è già presente nella lista `data`
            existing_doc = next((entry for entry in data if entry['id'] == doc_data['id']), None)

            if existing_doc:
                # Se già esiste, aggiorno
                data[data.index(existing_doc)] = doc_data
                print(f"Documento aggiornato nella lista: {doc_data}")
            else:
                # Se non esiste, aggiungo
                data.append(doc_data)
                print(f"Nuovo documento aggiunto alla lista: {doc_data}")

        return data

    except Exception as e:
        print(f"Errore nel recupero dei dati: {e}")
        return []


# Funzione per aggiornare la lista dei documenti in base ai cambiamenti
def update_local_data(change):
    global data
    doc_id = change.document.id
    doc_data = change.document.to_dict()
    doc_data['id'] = doc_id

    print(f"Aggiornamento per documento: {doc_id}")
    print(f"Dati del documento: {doc_data}")

    # Controllo se la data del documento è entro le prossime due ore
    if not is_within_next_two_hours(doc_data['data']):
        print(f"Documento con ID {doc_id} ignorato perché fuori dall'intervallo di tempo")
        return

    existing_doc = next((entry for entry in data if entry['id'] == doc_id), None)

    if existing_doc:
        # Se il documento è stato modificato, lo sostituisco
        if change.type.name == 'MODIFIED':
            data[data.index(existing_doc)] = doc_data
            print(f"Documento con ID {doc_id} aggiornato nella lista locale")
        # Se il documento è stato eliminato, lo rimuovo
        elif change.type.name == 'REMOVED':
            data.remove(existing_doc)
            print(f"Documento con ID {doc_id} rimosso dalla lista locale")
    else:
        # Se il documento non esiste e viene aggiunto, lo aggiungo alla lista
        if change.type.name == 'ADDED':
            data.append(doc_data)
            print(f"Nuovo documento con ID {doc_id} aggiunto alla lista locale")


def on_snapshot(col_snapshot, changes, read_time):
    print(f'Notifica di cambiamenti da Firestore al {read_time}:')
    global data
    for change in changes:
        doc_id = change.document.id
        doc_data = change.document.to_dict()
        doc_data['id'] = doc_id

        if 'data' not in doc_data:
            print(f"Documento con ID {doc_id} non ha un campo 'data', ignorato.")
            continue

        if change.type.name == 'ADDED':
            print(f"Nuovo documento aggiunto: {doc_id}")
            update_local_data(change)
        elif change.type.name == 'MODIFIED':
            print(f"Documento modificato: {doc_id}")
            update_local_data(change)
        elif change.type.name == 'REMOVED':
            print(f"Documento rimosso: {doc_id}")
            update_local_data(change)

    print(f"Stato attuale della lista globale `data`: {data}")


def setup_firestore_listener():
    print("Impostazione listener per Firestore...")
    collection_name = 'PostScheduled'
    collection_ref = db.collection(collection_name)

    # Aggiungi un listener per la collection
    collection_ref.on_snapshot(on_snapshot)


# Funzione principale che inizializza i dati e imposta il listener
def main():
    global data
    data = get_data_from_firebase()
    check_for_matching_time(data)
    setup_firestore_listener()

    # Mantiene il programma attivo per permettere al listener di funzionare
    while True:
        time.sleep(20)
        check_for_matching_time(data)


if __name__ == "__main__":
    main()
