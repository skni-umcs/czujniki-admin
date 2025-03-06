# Administration Service for Sensors

### This service is responsible for managing sensors and storing various technical information.

## How to run and test

```bash
docker compose up -d 
```

locally, whole API can be seen here:
```
localhost:8000/docs#
```

# What is used
## MQTT
MQTT is used for a two-way communication between the service and gateway.
### Valid MQTT messages received by service
#### Sensor Data
```json
{
    "sensor_id": "string",
    "rssi": 0,
    "cpu_temp": 0,
    "sensor_noise": 0
}
```
Right now, partially filled messages will not be processed.

### MQTT messages send by service
#### New frequency for sensor
```json
{
    "sensor_id": "string",
    "new_frequencies": 0
}
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
MQTT_TOPIC_RECEIVE=[mqtt topic for receiving data]
MQTT_TOPIC_SEND=[mqtt topic for sending data]
```

# Technical stuff
## Database Models
### Sensor:
 - Sensor Code (Working as UUID)
 - Human-readable name (assigned by admin user while adding a module)
 - Location (geo coordinates + faculty name) 
 - State (active/inactive/error) 
 - Frequency of sending data
 - Signal Power
 - CPU temperature
 - Sensor noise
 - Timestamp of lastly received data

### User:
 - UUID
 - Keycloak ID: ID from Keycloak
 - Login: User login received from Keycloak

### Log:
 - Timestamp
 - Message


