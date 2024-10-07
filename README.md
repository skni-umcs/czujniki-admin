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


Service can be integrated with Keycloak for authentication and authorization purposes.

## How to run

```bash
docker-compose up -d 
```

### Strange things
I assumed that keycloak and fastapi will be run in different docker containers
and I had to do a little workaround to make it work in one particular case:
- while making a request to get token from keycloak, I had to use `http://keycloak:8080` instead of `http://localhost:8080`
probably because it is made via fastapi itself, and it is not able to resolve `localhost` to `keycloak` container.
