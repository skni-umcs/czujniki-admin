# Backend for controlling modules with sensors

This project is a backend service for controlling modules 

Sensor model contains basic info:
 - Sensor Code (Working as UUID)
 - Human-readable name (assigned by admin user while adding a module)
 - Location (geo coordinates + faculty name)
 - State (active/inactive/error) 
 - Frequency of sending data
 - Signal Power
 - CPU temperature
 - Sensor noise
 - Timestamp of lastly received data

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

## Valid MQTT message format
```json
{
    "sensor_code": "string",
    "rssi": 0,
    "cpu_temp": 0,
    "sensor_noise": 0
}
```
### Right now partially filled messages will not be processed.

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
MQTT_TOPIC_RECEIVE=[mqtt topic for receiving data]
MQTT_TOPIC_SEND=[mqtt topic for sending data]
```

