import firebase_admin
from firebase_admin import credentials, firestore, auth

# Path to your Firebase admin SDK JSON file
cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Firestore instance
db = firestore.client()
