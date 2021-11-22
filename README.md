```


# File: README.md
# Created at 03/11/2021
```
## Environment

- docker
- docker-compose
- python3

## Structure of project

- conf:
  - supervisor: ```All configuration files to use the service run with cmd```
- src:
  - api: 
    - [endpoint]: 
      - urls: ``config route of endpoint``
      - controller: ``handle all api``
  - decorators: ```Auth, Cache, handle response, ...```
  - enums: ```Enums of service```
  - exceptions: ```Define and handle all exceptions```
  - helpers:
  - inside: ```inside service```
  - models: ```Define models in database```
  - schedule:
  - services: ```Service base on an object``` 
  - schemas: ```Define request and response data between client and server```
  - utils: 
  - workers: ```Workers of service```
  - consumer: ```Handle tasks```
  - producers: ```Functions for sending messages to Kafka```

### Notes

- Changes in docker-compose.yml: exposed port, image name, container name
- Change name service in config.py

### Use with docker, docker-compose

JUST RUN: `> docker-compose up -d --build`

### Run celery

```celery --app src.tasks worker -Q celery -l DEBUG -c 4```

## Health check

```curl -i <domain>/v1/<service>/common/health_check```

## Container env config:

```/webapps/service/.env```
