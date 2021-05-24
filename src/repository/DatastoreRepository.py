from .User import User
from google.cloud import datastore

_KIND = 'User'


class DatastoreRepository:

    def __init__(self):
        self.client = datastore.Client()

    def persist(self, user: User):
        kind = "Task"
        # The name/ID for the new entity
        name = "sampletask1"
        # The Cloud Datastore key for the new entity
        task_key = self.client.key(kind, name)

        # Prepares the new entity
        task = datastore.Entity(key=task_key)
        task["description"] = "Buy milk"

        # Saves the entity
        self.client.put(task)

        print(f"Saved {task.key.name}: {task['description']}")

    def load(self, key) :
        return {
            'profile': {
                'email': 'ricardofagodoy@gmail.com',
                'first_name': 'Ricky',
                'last_name': 'Godoy'
            }
        }
