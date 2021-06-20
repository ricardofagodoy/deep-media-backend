# Deep Media - Backend public APIs

### APIs designed to serve frontend https://app.deepmediaco.com and control connectors, configurations and optimizations.

## Important files/directories:

- **src**: Flask-based RESTish APIs to serve connectors, configurations and optimizations the simplest way possible.

- **run-local.sh/run-local-server.sh**: copy the `env-template.sh` and call it `env.sh` with your configuration. Run local runs pure Flask python, and server runs on gunicorn.

- **run-docker.sh**: builds image locally and runs it

- **install-cloud.sh**: script to install solution to Google Cloud Run.