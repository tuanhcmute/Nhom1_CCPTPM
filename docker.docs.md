### List docker images
```
docker images
```

### Remove docker image
```
docker rmi image_id
```

### Get log container
```
docker logs container_id
```

### List docker conatainer
```
docker ps
```
or
```
docker ps -a
```

### Remove docker container
```
docker rm container_id
```
or
```
docker rm -f container_id
```

### Build docker image
docker build --tag flask-python/api-dashboard:v1.0.0 .

### Create and run container
```
docker run \
--name api-dashboard-container \
-p 50001:50000 \
-d python/api-dashboard:v1.0.0
```

### Run container exits
```
docker start container_id
```

### Stop container is running
```
docker stop container_id
```

### Go to inside docker container
```
docker exec -it <container_id> <shell>
```

### Run docker compose
Build:
```
docker-compose -f ./docker-compose.yml up --build -d

```
Remove: 
```
docker-compose -f docker-compose.yml down
```
###