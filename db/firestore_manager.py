from firebase_config import get_firestore_db
from datetime import datetime

# Inizializza Firestore
db = get_firestore_db()

# Funzione per creare un documento per l'utente
def create_user_record(uid, user_data):
    try:
        # Crea il record per l'utente nella collezione Utenti
        db.collection('Utenti').document(uid).set(user_data)
        print(f"User record created for UID: {uid}")
    except Exception as e:
        print(f"Error creating user record: {e}")

# Funzione per creare un documento per i post pubblicati
def create_post_pubblicati_record(uid):
    try:
        # Crea un array vuoto per i post pubblicati
        db.collection('PostPubblicati').document(uid).set({
            'posts': []
        })
        print(f"PostPubblicati record created for UID: {uid}")
    except Exception as e:
        print(f"Error creating PostPubblicati record: {e}")

# Funzione per creare un documento per i post da pubblicare
def create_post_da_pubblicare_record(uid):
    try:
        # Crea un array vuoto per i post da pubblicare
        db.collection('PostDaPubblicare').document(uid).set({
            'posts': []
        })
        print(f"PostDaPubblicare record created for UID: {uid}")
    except Exception as e:
        print(f"Error creating PostDaPubblicare record: {e}")
