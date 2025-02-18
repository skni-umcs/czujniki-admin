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