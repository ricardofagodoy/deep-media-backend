from datetime import datetime
from repository.job_repository import JobRepository


class SchedulerRepository(JobRepository):

    def __init__(self, project_id: str, location_id: str, timezone_str: str, optimizers_topic: str, cron: str):

        if not all([project_id, location_id, timezone_str, optimizers_topic, cron]):
            raise Exception('Invalid scheduler configuration.')

    def get_scheduled_optimizations(self, uid):
        return [{
            'next_run': datetime.now(),
            'uid': uid,
            'type': 'google'
        }]

    def schedule_optimization(self, connector_type: str, uid):
        print('Created new job')

    def delete_scheduled_optimization(self, connector_type, uid):
        print('Job {} deleted')
