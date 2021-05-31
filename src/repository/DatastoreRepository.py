from google.cloud import datastore

_OPTIMIZATIONS_STORE = 'optimizations'
_CONNECTORS_STORE = 'connectors'
_CONFIGURATION_STORE = 'configurations'


class DatastoreRepository:

    def __init__(self):
        self.client = datastore.Client()

    def persist_connector(self, connector_type, configuration, uid):

        entity = datastore.Entity(self.client.key('User', uid, _CONNECTORS_STORE, connector_type))
        entity.update(configuration)

        self.client.put(entity)

    def load_connectors(self, uid):

        query = self.client.query(ancestor=self.client.key('User', uid), kind=_CONNECTORS_STORE)
        query.keys_only()

        response = [conn.key.name for conn in query.fetch()]

        return response

    def load_connector(self, connector_type, uid):
        return self.client.get(self.client.key('User', uid, _CONNECTORS_STORE, connector_type))

    '''
    def persist_configuration(self, configuration):

        if configuration['id']:
            configuration_cache = [c for c in DatastoreRepository.configuration_cache if c['id'] != configuration['id']].append(configuration)
        else:
            configuration['id'] = len(DatastoreRepository.configuration_cache) + 1
            DatastoreRepository.configuration_cache.append(configuration)

    def load_configuration(self):
        return DatastoreRepository.connectors_cache

    def persist(self):
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

    def load(self, key):
        return {
            'profile': {
                'email': 'ricardofagodoy@gmail.com',
                'first_name': 'Ricky',
                'last_name': 'Godoy'
            }
            '''
