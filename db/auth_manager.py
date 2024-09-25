from firebase_admin import auth
from firebase_config import get_auth

# Funzione di registrazione
def register_user(email, password):
    auth_service = get_auth()
    try:
        user = auth_service.create_user(
            email=email,
            password=password
        )
        print(f"User {email} registered with UID: {user.uid}")
        return user.uid
    except Exception as e:
        print(f"Error during registration: {e}")
        return None

# Funzione di login
def login_user(email, password):
    # Firebase Auth non gestisce direttamente il login (JWT-based).
    # Dovresti implementare un sistema di login lato client.
    pass

# Funzione per ottenere i dettagli dell'utente
def get_user(uid):
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
