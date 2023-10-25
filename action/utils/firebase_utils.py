from decouple import config
import pyrebase

_firebase_instance = None


def get_firebase_instance():
    global _firebase_instance
    if _firebase_instance is None:
        _firebase_instance = pyrebase.initialize_app({
            "apiKey": config('FIREBASE_API_KEY'),
            "authDomain": config('FIREBASE_AUTH_DOMAIN'),
            "projectId": config('FIREBASE_PROJECT_ID'),
            "storageBucket": config('FIREBASE_STORAGE_BUCKET'),
            "messagingSenderId": config('FIREBASE_MESSAGING_SENDER_ID'),
            "appId": config('FIREBASE_APP_ID'),
            "measurementId": config('FIREBASE_MEASUREMENT_ID'),
            "databaseURL": config('FIREBASE_DATABASE_URL')
        })
    return _firebase_instance
