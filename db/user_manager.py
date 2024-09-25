from auth_manager import register_user
from firestore_manager import create_user_record, create_post_pubblicati_record, create_post_da_pubblicare_record
from datetime import datetime


# Funzione per registrare un nuovo utente e creare i relativi documenti
def register_new_user(email, password, nome, cognome, telefono, prefisso):
    # Registra l'utente
    uid = register_user(email, password)

    if uid:
        # Struttura del documento per la collezione Utenti
        user_data = {
            "piano_abbonamento": "basic",  # O premium se ci sono vari piani
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "telefono": telefono,
            "prefisso": prefisso,
            "data_iscrizione": datetime.now(),
            "instagram": {"access_token": None},
            "facebook": {"access_token": None},
            "tiktok": {"access_token": None},
            "x": {"access_token": None},
            "linkedin": {"access_token": None},
        }

        # Crea i documenti nelle collezioni Firestore
        create_user_record(uid, user_data)
        create_post_pubblicati_record(uid)
        create_post_da_pubblicare_record(uid)
    else:
        print("Errore nella registrazione dell'utente.")
