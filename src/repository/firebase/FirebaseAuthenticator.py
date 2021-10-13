import firebase_admin
from typing import Dict
from firebase_admin import auth
from repository.authenticator import Authenticator
firebase_admin.initialize_app()


class FirebaseAuthenticator(Authenticator):

    def verify_id_token(self, token: str) -> Dict:
        return auth.verify_id_token(token)
