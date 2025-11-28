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

# Abilities
1. Sync with climate backend to get latest sensors count with their location.
2. Listening to MQTT messages from gateway with technical and climate data.
3. Storing service data in the database.
4. Two websocket endpoints for real-time data:
   - one for sensor network graph in service data
   - one for sensor general info
5. Background status checker for sensors to mark them offline if no data received in a while.
6. Authentication and authorization with either authentik or client credentials.

## Climate backend synchronization
Upon starting the app, it will synchronize with the climate backend to get the latest location data for each sensor. 

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
    "queue_fill": int,
    "collisions": int
}
```
For now, messages without collisions field will be processed normally.

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
SENSOR_OFFLINE_THRESHOLD=[time in seconds from last ping to consider a sensor offline]
SENSOR_SEND_RATE_SECONDS=[time in seconds between sensor data sends]
```



