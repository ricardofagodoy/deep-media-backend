from abc import abstractmethod, ABC
from typing import Dict


class Authenticator(ABC):

    @abstractmethod
    def verify_id_token(self, token: str) -> Dict:
        raise NotImplementedError()
