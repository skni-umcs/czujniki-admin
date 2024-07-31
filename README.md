# Backend for controlling sensors


```bash
docker-compose up -d 
```

### Strange things
I assumed that keycloak and fastapi will be run in different docker containers
and I had to do a little workaround to make it work in one particular case:
- while making a request to get token from keycloak, I had to use `http://keycloak:8080` instead of `http://localhost:8080`
probably because it is made via fastapi itself, and it is not able to resolve `localhost` to `keycloak` container.
