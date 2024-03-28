# DevOpsLab

Training repo for Docker, Docker Swarm, Kubernetes and other DevOps related technologies and topics.
Currently only Docker part present, other topics in active development.

# Docker basics

Add diagrams with Docker and VM comparison. Difference between image and container.


# Useful resources:

- 100+ Docker Concepts in 10 minutes
  https://www.youtube.com/watch?v=rIrNIzy6U_g
- Docker in 1 hour
  https://www.youtube.com/watch?v=pg19Z8LL06w
- Docker in 3 hours
  https://www.youtube.com/watch?v=3c-iBn73dDE


# Useful docker notes

do not use ```docker attach``` command, once you get out of it, it will close the main container shell that runs your app, effectively ending container functionality, can cause outage

```docker exec mycontainer ls /```
is better command (we send the command remotely from host VM)

best trick
```docker exec -it mycontainer /bin/bash```   this leaves your main shell intact when I exit, so does not cause an outage

you can build docker images from Docker file, but also from well working tweaked containers
that is great trick, but this is not recommended
it is better to fix the Dockerfile itself

images are static, read only

containers have option for read write access to the volume system





# Why use Docker

We do not have to use containers, apps running directly in VM are fine in general.
Especially databases under heavy load and monolith apps do not need to be packed in another layer of abstraction.

Docker and containers in general offer following benefits:

- process isolation
- deployment consistency (we start from clean images, image structure fully under developer control)
- granularity of microservices (app modules are typically not that complex as monolithical app)
- self healing, liveness probes
- partial degradation (app works in general, just payment gateway microservice went down)
- target VM retains old app images - super easy rollback in cse of outage, we just spin up old good container
- ability to limit resource usage for each container
- easy automated app deployments
- allows for fast app lifecycle iteration
- goes well with CI/CD build pipelines
- scaling - Docker Swarm, Kubernetes
- easy and quick rollback to older well functioning containers/images (including artefacts)
- docker containers are relatively easy to build and run (this changes with kubernetes though)
- provides level of abstraction - when expanding app functionality, we can create just new microservice -> thinking on API/microservice level
- allows for easy combination of different technologies (app can have both express and flask backends, can use multiple separate DBs - Postreg + Mongo). If having multiple technologies within one project is good idea, that is another question.
- app in container thinks it is running in regular VM (not entirely true, there are some docker specific directives app can call, such as ```host.docker.internal``` directive and Docker DNS), we can let app know it runs in container by injecting env variables
- app can be built by parts as Lego


Disadvantages:

- another level of abstraction
- larger attack surface
- has learning curve
- Kubernetes orchestration of containers can become very complex



Interesting topics not covered (yet):

- multi-stage builds
- container DNS
- advanced Docker networking
- SELinux, AppArmor




Ubuntu 22.04 prerequisites:

Install Docker daemon andd add your user to ```docker``` group.

```bash
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install docker docker-compose
sudo usermod -aG docker $USER
docker --version
docker-compose --version
```

And install pip so we can develop python apps locally before putting them into container.

```bash
sudo apt install python3-pip
```

## Docker cheatsheets
- https://quickref.me/docker.html
- https://github.com/wsargent/docker-cheat-sheet?tab=readme-ov-file

## Docker best practices
- https://docs.docker.com/develop/develop-images/guidelines/
- https://github.com/dnaprawa/dockerfile-best-practices
- https://www.youtube.com/watch?v=8vXoMqWgbQQ

best practices summary:
- use official and verified docker image (official node, python)
- do not use 'latest' tag, use specific tags (both for pull and for image creation)
- prefer smaller base images (eg. Alpine Linux, smaller attack surface), even official app images use various OSes as base, like node:17.0.1-alpine
- optimize caching Image Layers in Dockerfile (see with ```docker history myapp:1.0```), sequence of build commands is important (cache invaidation for higher levels), least changed data -> most frequently changed data
- exclude unneeded build directories and files (size, security implications), use .dockerignore file, multi-stage builds to reduce image size
- do not run containers with root privileges (from host VM side), do not run app in container as root user (from inside of the container)
- scan images for vulnerabilities (eg. via DockerHub ```docker scan myapp:1.0```), integrate scans into CI/CD pipelines
- validate Dockerfiles with Hadolint (alternatively www.fromlatest.io)


# Docker lab section

Topics covered:
basic Docker setup, data persistence, logging, resource allocation, best practices, security.



Project outline:
we will be using basic web app with flask based frontend and backend.
In subsequent projects we will make the architecture of the app more and more complex.


Project structure:
```bash
frontend ... port 8080
backend  ... port 5100
optional reverse proxy ... port 80, 443
```

start frontend/backend normally

```bash
frontend: python3 app.py
backend:  python3 app.py
```

backend is writing data to sqlite database "locally". 
Term "local" can have different meanings in context of containerised apps. 

## scenario_1

Basic flask app

build images locally

```bash
docker build -t
docker build -t
```

start frontend and backend containers

```bash
docker run -it -e -p 5100:5100 your-backend-docker-image
docker run -it -e ENV=prod --name frontend -p 8080:8080 your-frontend-docker-image
docker run -d -e ENV=prod --name frontend -p 8080:8080 your-frontend-docker-image
```

verify env var is present within container
```docker exec -it frontend bash -c 'echo "$ENV"'```

we can also use ./env file via --env-file directive (so secrets are not in shell history)


## scenario_2

Enhanced flask app with persistence and best practices. Plus some basic security considerations.
Dir mounts and logging to VM file. Optimized layer build sequence.



## Backend

```bash
curl -X POST \
  http://localhost:5100/posts \
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




## General Docker notes

```bash
docker run -p 80:80 myimage     # port linking
docker run -it -p 80:80 myimage   # runs interactively (we can see logs rolling)
docker run -d -p 80:80 myimage   # spins up container in background
docker run -d --name mycontainer -p 80:80 myimage   # assign custom name to container


docker ps   # shows running containers
docker ps -a  # shows all containers

docker stop mycontainer
docker kill mycontainer



docker inspect mycontainer # shows detailed info about container (running/stopped)


docker stats   # resource usage for all cotainers
docker top mycontainer  # show running processes inside container

docker network ls # shows docker networks


docker logging:
docker logs -f mycontainer   # equivalent of tail -f on the container logs
```

troubleshooting commands
```bash
docker attach mycontainer # do not use, will likely cause container outage, takes over main shell that runs the actual app
docker exec mycontainer whoami  # execute command within container
docker exec -it mycontainer /bin/bash    # favourite t-shooting command


docker images
docker rmi <image_name>

docker system prune # removed hanging images and residual stopped containers (can clean up lots of disk space, relatively safe command), some admins run the command from cron daily
```


## Stress test

Limiting container resource usage

simple stress test Dockerfile:
```docker
FROM ubuntu
RUN apt-get update && apt-get install stress
CMD stress $var
```

```bash
docker build -t docker-stress .

remove all other containers
docker rm -f $(docker -a -q)

container is very resource hungry
docker run --rm -it -e var="--cpu 6 --timeout 40" docker-stress   # test runs for 40 seconds
docker stats

we limit hungry container on docker level
docker run --rm -it -e var="--cpu 6 --timeout 40" --cpus 1 --name docker-stress-cont docker-stress
docker stats
```


```bash
docker stats someimage

docker run --cpus 2 <docker-image>
docker run --cpushares 256 <docker-image>    # by default 1024 cpushares, if only 1 container running, Docker will give it all cpushares even if limited by parameter, so Docker makes override

docker run --memory 512MB --memory-swap 1024MB <docker-image>  # swap number has to be higher than memory, otherwise no swap gets allocated
```

memory limits are best combined with liveness probes, so container does not get stuck with out of memory condition



Memory limitation

```docker
docker run --rm -it -e var="--vm 2 --vm-bytes 128MB --timeout 40" --name docker-stress-cont docker-stress 
docker stats


docker run --rm -it -e var="--vm 2 --vm-bytes 128MB --timeout 40" --memory 512 --name docker-stress-cont docker-stress 
docker stats
```

docker can also limit container I/O disk operations



# Docker security

Docker does not provide the same sandboxing as regular VM does.
Docker daemon is just a process running inside VM and Docker is managed by VM kernel.
Docker daemon typically runs under root user (from VM perspective) and users that have access to Docker daemon are typically members of ```docker``` group. Making them essentially system admins -> access to ```docker``` group needs to be limited. From security standpoint, do not treat containers as micro-VMs.

Docker engine generates several linux namespaces, such as: process ID (PID), mount (MNT), networking (NET), USER namespace, ...
linux namespaces are meant for isolation purposes

Best security docker practices:

- keep docker engine patched regularly
- securing docker socket (```/var/run/docker.sock```) only accessible by root and users in ```docker``` group (sysadmins, not devs)
- docker does not fix bad/insecure app code
- always set unprivileged user (add user to Dockerfile)
- when running Docker, use ``--user``` flag to docker run command
- set nologin for root user in container
- download only official images from container repos (such as DockerHub)
- start docker container with ```no-new-privileges``` to avoid rights escalation
- mount files to container in read only where feasible (--mount source=...,readonly)
- run whole container in read only where feasible ```docker run --read-only <myimage> sh -c 'echo "Testing" > /tmp/test'```
- do not include passwords, API keys, RSA keys into Dockerfile/image
- read a book on Docker security
- ```COPY . .``` command is recursive, you can unknowingly copy sensitive data to image, make sure you use .dockerignore file to limit what we copy to image
- limit available resources for containers - CPU, RAM, Disk I/O, helps mitigate Denial of service attack impact on given microservice.
- drop container capabilities (```docker run -d -it --cap-drop=chown <myimage>```)
- handling secrets - familiarize yourself with ```docker secret``` command
- use docker image tags consistently (```1.1.2-prod```, ```1.1.2-dev```, ```LABEL "version"="1.1.2-dev"``` directive in Dockerfile, can be seen with ```docker inspect <myimage>``` command)


```docker
FROM alpine

RUN addgroup -S secureusers && adduser -S secureuser -G secureusers

# execute any root based commands before switching to unprivileged user
USER secureuser
```


Run container as specific user
```bash
docker run 
docker run --user 5000:500   # userid:groupid
```

no privileges escalation

```bash
docker run -d -it --security-opt=no-new-privileges <myimage>
```

uses linux kernel feature that prevents priv escalation, our docker app will not be able to use ```setuid```
for example (```setuid``` allows for rights escalation). This helps to prevent container breakout to host VM.





# Other

To restart docker container regularly we can use cron.
For example more complex streamlit python apps benefit from restarting from time to time.



Cron Jobs (for Linux users): You can use a cron job to schedule a weekly restart of your Docker container. Open your crontab file with the command crontab -e and add a line like this:

```bash
0 0 * * 0 docker restart container_name_or_id
```

This will restart the specified Docker container at 00:00 (midnight) every Sunday. Remember to replace container_name_or_id with the name or ID of your Docker container.
Requires container with static name.




# Docker development

Personal observation when developing on Docker. 

Port mapping 
we can run app on its default port in container and expose it on VM on different port.
So for example flask runs by default on port 5000, so the mapping would be ```-p 5001:5000```.

But since building Docker images takes time, it would delay us in the development.
Especially React/NextJS frontend image builds are heavy on resources, especially when we use Linux running in Virtual box as dev machine. You will see lots of Disk IO wait times and system interrupts during builds.


So turns out it is convenient to have apps running locally during dev on the same port that container would be using. On main dev VM there would also be NGINX reverse proxy aware of the app/container ports.

so lets say we have frontend on port 3000, flask backend on 5000 and express backend on 5000

then we would remap the apps themselves to ports corresponding to final container setup and let revese proxy to be aware of the port architecture
so it would be 3000, 5100 and 5200. This way we can run dev tests easily without containers and we save lots of time.

So basically, app architecture should be the same with and without containers. You can let app know it runs within container with injected env vars.



# Other useful Docker commands

docker ps -a  # list all containers (even stopped and paused ones)
docker pause mycontainer   # pauses container
docker unpause mycontainer # unpauses container
docker restart mycontainer # restarts container
docker stop mycontainer # stops container
docker start mycontainer # starts contaner
docker stop -t 10 mycontainer # stops gracefully (SIGTERM), force stop later if need be (SIGKILL)
docker kill mycontainer # force stop container
docker logs mycontainer # shows logging for containers


## Image and Docker hub related commands

docker login
docker image ls  # (docker images)
# create your Dockerfile and then in the same directory run:
docker image build --tag dockerhubuser/myimage:v0.1
# alternatively
docker build -t myimage:v0.1
# then push to DockerHub repo if needed
docker push dockerhubuser/myimage:v0.1

# pull our image from registry if needed
docker pull dockerhubuser/myimage:v0.1


#remove the image locally
docker image rmi dockerhubuser/myimage:v0.1
# alternatively
docker rmi dockerhubuser/myimage:v0.1


## Docker volumes for persistence
3 types: host, anonymous and named volumes (use named volumes for production ideally)

host volumes (-v hostVM:container)
docker run -v /home/mount/data:/var/lib/mysql/data --name <container> <image>

Anonymous Volumes (-v /container/dir)
docker run -v /var/lib/mysql/data --name <container> <image>
some random hash volume will be created under /var/lib/docker/volumes/ directory on host VM

Named volumes (-v name:/container/dir) 
need to create docker volume first
docker volume create volume_1
docker volume ls
docker volume inspect volume_1
docker run -v <vol_name>:/var/lib/mysql/data --name <container> <image>
docker volume rm volume_1 # remove volume when not needed
docker volume ls

Named volumes go well with docker-compose files, easy to define shared dir for containers (for example for logging)




# Kubernetes (general notes)

kubernetes is state machine


pods are dynamic, but services are static, services have static IP address - serves as load balancer for pods/containers

node port service exposes Ips of worker nodes, not really good practice
LoadBalancer service is much better, but this is for cloud providers

not sure how to actually do it on VM


ingress just needs one cloud load balancer, so it is much cheaper
instructor always always goes for ingress (like nginx, traefik)



also minikube has ingress with one simple command (builtin nginx ingress)





