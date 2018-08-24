# Code Challenge

The code of the following solution is based on this
[flask-boilerplate](https://github.com/tko22/flask-boilerplate)

## Usage

To try this, you need [docker](https://docs.docker.com/install/) and
[docker-compose](https://docs.docker.com/compose/install/#install-compose)

Once installed build the docker images(the flask and postgres database):

    docker-compose up -d

Now the API is available in the http://localhost:5000 url.

## Test

To run the tests you need access to the app container's bash:

    docker-compose exec app bash

Now with [pipenv](https://pipenv.readthedocs.io/en/latest/) install pytest and
run the tests

    pipenv install --dev
    pipenv run pytest tests
