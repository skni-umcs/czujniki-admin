# Backend for controlling modules with sensors

This project is a backend service for controlling modules 

Sensor model contains basic info:
 - UUID
 - Human-readable name (assigned by admin user while adding a module)
 - Location (geo coordinates + faculty name)
 - State (active/inactive/error)
 - Last timestamp of received information
 - Signal Power

It also stores information about signal power for each module (with timestamp).

## What is used
- **MQTT** - background listener waiting for gateway information about sensors
- **Keycloak** - OAuth for authentication and authorization

## How to run

```bash
docker-compose up -d 
```

## Docs
If run locally, whole API can be seen here:
```
localhost:8000/docs#
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

