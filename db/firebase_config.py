import firebase_admin
from firebase_admin import credentials, firestore, auth

# Inizializza l'app Firebase con le credenziali appropriate
def initialize_firebase():
    cred = credentials.Certificate("path_to_your_firebase_credentials.json")
    firebase_admin.initialize_app(cred)
    print("Firebase initialized.")

# Inizializza Firestore
def get_firestore_db():
    return firestore.client()

# Funzione per inizializzare Firebase Authentication
def get_auth():
    return auth
