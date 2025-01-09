import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK with the credentials
cred = credentials.Certificate('path_to_your_firebase_credentials.json')
firebase_admin.initialize_app(cred)
