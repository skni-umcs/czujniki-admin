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
## Climate backend synchronization
The service synchronizes with the climate backend to get the latest climate data for each sensor. 

For now, this is done once on a startup. Later it will be done periodically.
## MQTT
MQTT is used for a two-way communication between the API and gateway.
### Valid MQTT messages received by service
#### Sensor Data
```json
{
    "source_id": int,
    "cpu_temp": int,
    "noise": int,
    "free_heap": int,
    "raw_packet": str,
    "hop_data": [[int,int],...],
    "timestamp": time/str,
    "queue_fill": int
}
```
Right now, partially filled messages will not be processed.

### MQTT messages send by service
#### New frequency for sensor
```json
{
    "sensor_id": str,
    "new_frequency_temp": 0
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
AUTHENTIK_SERVER_URL=[authentik server url]
AUTHENTIK_APP_NAME=[authentik application name]
AUTHENTIK_CLIENT_ID=[authentik client id]
AUTHENTIK_ALGORITHM=[authentik algorithm, e.g. RS256]
MQTT_CLIENT=[mqtt client id]
MQTT_BROKER=[mqtt broker url]
MQTT_PORT=[mqtt broker port]
MQTT_TOPIC_RECEIVE=[mqtt topic for receiving data]
MQTT_TOPIC_SEND=[mqtt topic for sending data]
```



