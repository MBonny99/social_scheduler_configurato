from firebase_config import get_firestore_db

db = get_firestore_db()

# Funzione per aggiungere un post da pubblicare
def add_post_da_pubblicare(uid, post_data):
    try:
        # Aggiorna l'array di posts nella collezione PostDaPubblicare
        db.collection('PostDaPubblicare').document(uid).update({
            "posts": firestore.ArrayUnion([post_data])
        })
        print(f"Post aggiunto per l'utente {uid} in PostDaPubblicare.")
    except Exception as e:
        print(f"Errore durante l'aggiunta del post: {e}")

# Funzione per aggiungere un post pubblicato
def add_post_pubblicato(uid, post_data):
    try:
        # Aggiorna l'array di posts nella collezione PostPubblicati
        db.collection('PostPubblicati').document(uid).update({
            "posts": firestore.ArrayUnion([post_data])
        })
        print(f"Post pubblicato aggiunto per l'utente {uid}.")
    except Exception as e:
        print(f"Errore durante l'aggiunta del post pubblicato: {e}")
