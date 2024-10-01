from flask import Flask, request, jsonify, render_template, redirect
import firebase_admin
from firebase_admin import credentials, auth
import requests


# Configura l'app Flask
app = Flask(__name__)

# Inizializza Firebase Admin SDK per il backend
cred = credentials.Certificate("socialscheduler-b-firebase-adminsdk-z74d8-12256d992c.json")
firebase_admin.initialize_app(cred)


# Rotte per le pagine HTML
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/scheduler')
def dashboard():
    return render_template('scheduler.html')


# Rotta protetta
@app.route('/api/dashboard', methods=['POST'])
def api_dashboard():
    id_token = request.headers.get('Authorization')  # Ricevi il token dal frontend
    if not id_token:
        return jsonify({"error": "Token non fornito"}), 403

    try:
        # Verifica il token ricevuto dal frontend
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({"message": f"Accesso consentito per l'utente {uid}"})
    except Exception as e:
        return jsonify({"error": "Token non valido o scaduto", "details": str(e)}), 403


if __name__ == '__main__':
    app.run(debug=True)
