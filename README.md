# DevOpsLab
repo for Docker, Kubernetes and other DevOps related topics


Ubuntu 22.04 prerequisites:

```bash
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install docker docker-compose
sudo usermod -aG docker $USER
docker --version
docker-compose --version
```

```bash
sudo apt install python3-pip




```


## Backend

```bash
curl -X POST \
  http://localhost:5000/posts \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Example Title",
    "content": "This is an example content for the post."
}'

docker build -t flask-backend .

docker run -d -p 5000:5000 flask-backend
```

## Frontend

```bash
docker build -t flask-frontend .
docker run -d -p 80:80 flask-frontend

```