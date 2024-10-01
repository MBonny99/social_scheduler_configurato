from google.cloud import firestore
from datetime import datetime, timedelta
import time

# Inizializza il client Firestore
db = firestore.Client()
collection_time = 120

#TODO
# IMPLEMENTARE IL LISTNER AL POSTO DI CICLI ETC....


# Funzione per ottenere i dati da Firestore
def get_data_from_firebase():
    print("Chiamata Firestore per recuperare i dati...")

    # Specifica il nome della tua collection
    collection_name = 'PostScheduled'  # Cambia con il nome reale della collection

    
    try:
        # Ottieni l'ora attuale e aggiungi 2 ore
        current_time = datetime.now().replace(second=0, microsecond=0)
        end_time = current_time + timedelta(minutes=collection_time)

        # Converti le date in stringhe nel formato YYYY-MM-DD HH:mm:ss
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        # Stampa i tempi per il debugging
        print(f"Data e ora attuale: {current_time_str}")
        print(f"Data e ora +tempo: {end_time_str}")

        # Usa correttamente where() per i filtri temporali
        collection_ref = db.collection(collection_name).where(
            'data', '>=', current_time_str
        ).where(
            'data', '<', end_time_str
        )

        # Recupera i documenti dalla collection
        docs = collection_ref.get()
        data = []

        for doc in docs:
            doc_data = doc.to_dict()  # Converte il documento in un dizionario
            doc_data['id'] = doc.id  # Aggiunge l'ID del documento ai dati
            data.append(doc_data)
            print(f"Documento recuperato: {doc_data}")

        print(f"Dati recuperati da Firestore: {data}")
        return data
    except Exception as e:
        print(f"Errore nel recupero dei dati: {e}")
        return []

# Funzione per verificare se c'è una corrispondenza tra l'orario attuale e i dati recuperati
def check_for_matching_time(data):
    current_time_str = datetime.now().replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    to_remove = []  # Lista di elementi da rimuovere dopo la corrispondenza

    for entry in data:
        event_time_str = entry['data']  # Ora l'event_time è una stringa
        if current_time_str == event_time_str:
            print(f"Evento trovato con ID {entry['id']} alle {event_time_str}")
            socials = entry['social']
            for social in socials:
                print('creato il post per il social : ' + social)
            to_remove.append(entry)  # Aggiungi l'elemento alla lista per rimuoverlo

    # Rimuovi gli eventi trovati dalla lista principale
    for entry in to_remove:
        data.remove(entry)
        print(f"Evento con ID {entry['id']} rimosso dalla lista")

# Funzione principale che esegue le operazioni ogni minuto e aggiorna i dati ogni 2 ore
def main():
    data = get_data_from_firebase()  # Recupero iniziale dei dati
    last_fetch_time = datetime.now()

    while True:
        # Verifica se sono passate 2 ore dall'ultimo fetch
        if datetime.now() >= last_fetch_time + timedelta(minutes=collection_time):
            data = get_data_from_firebase()  # Aggiorna i dati
            last_fetch_time = datetime.now()  # Aggiorna il tempo dell'ultimo fetch

        # Controlla ogni minuto per vedere se c'è un evento che coincide con l'orario attuale
        check_for_matching_time(data)

        # Attendi 1 minuto prima di eseguire nuovamente il controllo
        time.sleep(60)

# Avvio della funzione principale
if __name__ == "__main__":
    main()
