# Backend for controlling modules with sensors

This project is a backend service for controlling modules 

Module model contains basic info:
 - UUID
 - Human-readable name (assigned by admin user while adding a module)
 - Location (geo coordinates + faculty name)
 - State (active/inactive/error)
 - Last timestamp of received information
 - Signal Power

This Backend gives the ability to:
- Add new modules 
- Remove modules
- Update modules (eg. deactivate, change name)

It also stores information about signal power for each module (with timestamp).

Service is integrated with Keycloak for authentication and authorization purposes.

## How to run

```bash
docker-compose up -d 
```

## .env file is required to run the service:
```bash
DB_HOST=[database host]
DB_PORT=[database port]
DB_USER=[database username]
DB_PASSWORD=[database user password]
DB_NAME= [database name]
ROOT_PATH=[root path for the service, should be set to '/']
KEYCLOAK_SERVER_URL=[keycloak server url]
KEYCLOAK_REALM=[keycloak realm]
KEYCLOAK_ALGO=[keycloak algorithm]
MQTT_CLIENT=[mqtt client id]
MQTT_BROKER=[mqtt broker url]
MQTT_PORT=[mqtt broker port]
MQTT_TOPIC=[mqtt topic]
```