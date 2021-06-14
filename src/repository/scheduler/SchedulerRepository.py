import json
from pytz import timezone
from google.api_core.exceptions import NotFound, AlreadyExists
from google.cloud import scheduler
from google.cloud.scheduler_v1 import CreateJobRequest, ListJobsRequest
from repository.job_repository import JobRepository


class SchedulerRepository(JobRepository):

    def __init__(self, project_id, location_id, timezone, service_account_email, optimizers_endpoint, cron):

        if not all([project_id, location_id, timezone, service_account_email, optimizers_endpoint, cron]):
            raise Exception('Invalid scheduler configuration.')

        self.timezone = timezone
        self.service_account_email = service_account_email
        self.optimizers_endpoint = optimizers_endpoint
        self.cron = cron
        self.parent = f"projects/{project_id}/locations/{location_id}"
        self.client = scheduler.CloudSchedulerClient()

    def get_scheduled_optimizations(self, uid):

        jobs = self.client.list_jobs(
            request=ListJobsRequest({
                "parent": self.parent
            })
        )

        return [{
            'next_run': job.schedule_time.astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M'),
            **json.loads(job.http_target.body)
        } for job in jobs]

    def schedule_optimization(self, connector_type: str, uid):

        job = {
            'name': self.__build_name(uid, connector_type),
            'http_target': {
                'uri': self.optimizers_endpoint,
                'http_method': 1,
                "headers": {
                    "Content-type": "application/json",
                },
                'body': json.dumps({
                    'uid': uid,
                    'type': connector_type
                }).encode('utf-8'),
                "oidc_token": {
                    "service_account_email": self.service_account_email
                },
            },
            'schedule': self.cron,
            'time_zone': self.timezone
        }

        try:
            response = self.client.create_job(
                request=CreateJobRequest({
                    "parent": self.parent,
                    "job": job
                })
            )

            print('Created new job: {}'.format(response.name))
        except AlreadyExists:
            print('Job {} already exists'.format(job['name']))

    def delete_scheduled_optimization(self, connector_type, uid):

        name = self.__build_name(uid, connector_type)

        try:
            self.client.delete_job(name=name)
            print('Job {} deleted'.format(name))
        except NotFound:
            print('Job {} not found'.format(name))

    def __build_name(self, uid, connector_type):
        return '%s/jobs/%s-%s' % (self.parent, uid, connector_type)
