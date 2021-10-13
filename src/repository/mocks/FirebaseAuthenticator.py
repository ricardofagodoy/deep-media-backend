from typing import Dict
from repository.authenticator import Authenticator


class FirebaseAuthenticator(Authenticator):

    def verify_id_token(self, token: str) -> Dict:
        return {'uid': 'uid'}
