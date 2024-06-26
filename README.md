# DevOpsLab

Training repo for Docker, Docker Swarm, Kubernetes and other DevOps related technologies and topics.
Currently only Docker part present, other topics in active development.

## Docker basics

Docker is a platform that uses containers to package and run applications with all their dependencies, making them portable and consistent across different environments. Unlike virtual machines (VMs) that virtualize entire operating systems, Docker containers share the host OS kernel, making them more lightweight and resource-efficient. While Docker provides efficient and faster deployment, VMs offer stronger isolation by running separate OS instances.

TODO:
Add diagrams with Docker and VM comparison. Difference between image and container.


## Useful Docker resources:

- 100+ Docker Concepts in 10 minutes
  https://www.youtube.com/watch?v=rIrNIzy6U_g
- Docker in 1 hour
  https://www.youtube.com/watch?v=pg19Z8LL06w
- Docker in 3 hours
  https://www.youtube.com/watch?v=3c-iBn73dDE




# Why use Docker

We do not have to use containers, apps running directly in VM are fine in general.
Especially databases under heavy load and monolith apps do not need to be packed in another layer of abstraction.

Docker and containers in general offer following benefits:

- process isolation
- deployment consistency (we start from clean images, image structure fully under developer control)
- granularity of microservices (app modules are typically not that complex as monolithical app)
- self healing, liveness probes
- partial service degradation (app works in general, just payment gateway microservice went down)
- target VM retains old app images - super easy rollback in cse of outage, we just spin up old good container
- ability to limit resource usage for each container
- (easier) automated app deployments
- allows for fast app lifecycle iteration
- goes well with CI/CD build pipelines
- scaling - Docker Swarm, Kubernetes
- easy and quick rollback to older well functioning containers/images (including artefacts)
- docker containers are relatively easy to build and run (this changes with kubernetes though)
- provides level of abstraction - when expanding app functionality, we can create just new microservice -> thinking on API/microservice level
- allows for easy combination of different technologies (app can have both express and flask backends, can use multiple separate DBs - Postgres, Mongo). If having multiple technologies within one project is good idea, that is another question.
- app in container thinks it is running in regular VM (not entirely true, there are some docker specific directives app can call, such as ```host.docker.internal``` directive and Docker DNS), we can let app know it runs in container by injecting env variables
- static security scanning of each image (easy to see vulnerabilities of you app in given build), we can see security vulnerabilities per image layer
- app can be built by parts as Lego


Disadvantages:

- another level of abstraction
- larger attack surface
- has learning curve
- Kubernetes orchestration of containers can become very complex



Interesting topics not covered (yet):

- multi-stage builds (to save disk space)
- container DNS
- advanced Docker networking
- SELinux, AppArmor (just basics covered)


### Lab prerequisites

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


## Useful docker notes

Do not use ```docker attach``` command, once you get out of it, it will close the main container shell that runs your app, effectively ending container functionality, can cause outage

```docker exec mycontainer ls /```
is better command (we send the command remotely from host VM)

best trick
```docker exec -it mycontainer /bin/bash```   this leaves your main shell intact upon exit, so does not cause an outage on running container

you can build docker images from Docker file, but also from well working tweaked containers
that is great trick, but this is not recommended in general
it is better to fix the Dockerfile itself

images are static, read only

containers have option for read write access to the volume system


## Docker cheatsheets
- https://quickref.me/docker.html
- https://github.com/wsargent/docker-cheat-sheet?tab=readme-ov-file

## Docker best practices
- https://docs.docker.com/develop/develop-images/guidelines/
- https://github.com/dnaprawa/dockerfile-best-practices
- https://www.youtube.com/watch?v=8vXoMqWgbQQ

Best practices summary:
- use official and verified docker image (official nodejs, python)
- do not use 'latest' tag, use specific tags (both for pull and for image creation)
- prefer smaller base images (eg. Alpine Linux, smaller attack surface), even official app images use various OSes as base, like node:17.0.1-alpine
- optimize caching Image Layers in Dockerfile (see with ```docker history myapp:1.0```), sequence of build commands is important (cache invaidation for higher levels), least changed data -> most frequently changed data
- exclude unneeded build directories and files (size, security implications), use .dockerignore file, multi-stage builds to reduce image size
- do not run containers with root privileges (from host VM side), do not run app in container as root user (from inside of the container)
- scan images for vulnerabilities (eg. via DockerHub ```docker scan myapp:1.0```), integrate scans into CI/CD pipelines
- validate Dockerfiles with Hadolint (alternatively www.fromlatest.io)


# Docker lab section

Topics covered:
basic Docker setup, data persistence, logging, resource allocation, best practices, security, healthcheck probes.



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

## Note
Regarding Docker Compose commands.
if 
```docker-compose up``` 
doesn't work, then use command without dash
```docker compose up```


## scenario_0

Super simple flask app

Build image locally (from scenario dir)

```bash
cd scenario_0
docker build -t myimage .
```

Start container interactively

```bash
docker run -it --rm --name simple-app -p 8000:8000 myimage
```

Alternatively handle with docker compose
```bash
docker-compose up
```

Check with curl
```bash
curl http://localhost:8000/
```

## scenario_1

Basic flask app that is functional, but has numerous build and security related issues.

Build images locally

```bash
cd scenario_1

docker-compose build
docker-compose up # performs build if needed

# direct builds in respective directories
cd backend
docker build -t backend-img .

cd frontend
docker build -t frontend-img .
```

start frontend and backend containers directly, no need to `cd` to respective dirs once images are built

```bash
docker run -it --rm --name backend -p 5100:5100 backend-img
docker run -it --rm --add-host=host.docker.internal:host-gateway -e ENV=prod --name frontend -p 8080:8080 frontend-img
# daemonized example
docker run -d <other params>
```

Check functionality with browser on http://localhost:8080

verify env var is present within container
```docker exec -it frontend bash -c 'echo "$ENV"'```

we can also use ./env file via --env-file directive (so secrets are not in shell history)


Check data persistence after just killing docker-compose, `docker-compose down`, `docker system prune`. And then starting the containers back up. 




## scenario_2

Enhanced flask app with data persistence and "best practices" (better practices).
Dir mounts and logging to VM file. Optimized layer build sequence.
Specific library version numbers in `requirements.txt`.


Build images locally

```bash
cd scenario_2

docker-compose build
docker-compose up # performs build if needed

# direct builds in respective directories
cd backend
docker build -t backend-img:v2 .

cd frontend
docker build -t frontend-img:v2 .
```

Start frontend and backend containers directly, no need to `cd` to respective dirs once images are built

```bash
mkdir -p /home/$USER/data
mkdir -p /home/$USER/logs

# backend
docker run -it --rm --name backend_v2 -p 5100:5100 \
  -v /home/$USER/data:/app/data \
  -v /home/$USER/logs:/app/logs \
  backend-img:v2


# frontend
docker run -it --rm --add-host=host.docker.internal:host-gateway -e ENV=prod \
-v /home/$USER/logs:/app/logs \
--name frontend_v2 \
-p 8080:8080 \
frontend-img:v2



# daemonized example (-d instead of -it)
docker run -d <other params>
```

We can test our backend API with `curl` if needed.

```bash
curl -X POST \
  http://localhost:5100/posts \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Example Title",
    "content": "This is an example content for the post."
}'
```


## Security template

Quick build of hardened image/container with simple flask app using basic security measures.


```bash
cd security-template

docker build -t secure-img:v1 .

docker run -it --rm --name secure_v1 -p 8000:8000 secure-img:v1

```

Try to get into the container and switch to root user.
```bash
docker exec -it secure_v1 /bin/bash

```

Now we have issues getting to root shell and by default we get to default nonprivileged user shell.
Without root shell removal, we would be able to switch to root without password. 
Attacker cannot install any other tools with apt/pip.
This will cause issues though if we need to troubleshoot directly within our container since our privileges will be limited.

```bash
coil@devVM:~/Desktop/DevOpsLab/security-template$ curl http://localhost:8000
Hello, Docker!
coil@devVM:~/Desktop/DevOpsLab/security-template$ docker exec -it security_v1 /bin/bash
appuser@452535828ff4:/app$ ls
Dockerfile  __pycache__  app.py  requirements.txt
appuser@452535828ff4:/app$ su
Password: 
su: Authentication failure
appuser@452535828ff4:/app$ sudo su -
bash: sudo: command not found
appuser@452535828ff4:/app$ su -
Password: 
su: Authentication failure
appuser@452535828ff4:/app$ apt-get install curl
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
appuser@452535828ff4:/app$
appuser@452535828ff4:/app$ pip install requests
WARNING: The directory '/home/appuser/.cache/pip' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you should use sudo's -H flag.
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: requests in /usr/local/lib/python3.8/site-packages (2.25.1)
Requirement already satisfied: chardet<5,>=3.0.2 in /usr/local/lib/python3.8/site-packages (from requests) (4.0.0)
Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.8/site-packages (from requests) (2.10)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.8/site-packages (from requests) (1.26.18)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.8/site-packages (from requests) (2024.2.2)
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied: '/home/appuser'
Check the permissions.

appuser@452535828ff4:/app$ 
```

We can still get access to container root user from host VM.

Note: it is unclear why root now has shell when we specified /sbin/nologin, this will need further investigation. Possibly managed by Docker daemon.

```bash
root@ae32643496be:/etc# coil@devVM:~/Desktop/DevOpsLab/security-template$ docker exec -it -u root secure_v1 /bin/bash
root@197c6180089c:/app# whoami
root
root@197c6180089c:/app# ls
Dockerfile  __pycache__  app.py  requirements.txt
root@197c6180089c:/app# 
```


## Stress test

Limiting container resource usage

Simple stress test Dockerfile:
```docker
FROM ubuntu
RUN apt-get update && apt-get install stress
CMD stress $var
```

```bash
docker build -t docker-stress .

#remove all other containers
docker rm -f $(docker -a -q)

#container is very resource hungry
docker run --rm -it -e var="--cpu 6 --timeout 40" docker-stress   # test runs for 40 seconds
docker stats

#we limit resource hungry container on docker level
docker run --rm -it -e var="--cpu 6 --timeout 40" --cpus 1 --name docker-stress-cont docker-stress
docker stats
```


```bash
docker stats <somecontainer>

docker run --cpus 2 <docker-image>
docker run --cpushares 256 <docker-image>    # by default 1024 cpushares, if only 1 container running, Docker will give it all cpushares even if limited by parameter, so Docker makes override

docker run --memory 512MB --memory-swap 1024MB <docker-image>  # swap number has to be higher than memory, otherwise no swap gets allocated
```

Memory limits are best combined with liveness probes, so container does not get stuck with out of memory condition



Memory limitation

```bash
docker run --rm -it -e var="--vm 2 --vm-bytes 128MB --timeout 40" --name docker-stress-cont docker-stress 
docker stats


docker run --rm -it -e var="--vm 2 --vm-bytes 128MB --timeout 40" --memory 512 --name docker-stress-cont docker-stress 
docker stats
```

Docker can also limit container I/O disk operations.






## Docker networking

When using `host.docker.internal` trick, you might encounter issues communicating between containers.
Eg. one backend container having issues contacting second backend container running on different port in different container.

How to t-shoot:
using ```docker exec``` run curl from within the container like

```bash
curl "http://host.docker.internal:5000/api/healthcheck"
```

(where the other container runs on port 5000)



Likely firewall will be causing the issues.

```bash
sudo ufw status

sudo ufw allow <port>   # maybe not needed and exposes port to the outside

sudo ufw allow in on docker0

sudo ufw reload

sudo ufw status
```


## What is 'localhost' ?

While dealing with containers, we need to be careful about what we mean by `localhost`.
When running the app on host VM, the localhost is the VM itself. Such app can reach other apps running on different ports without issues.

But in case we are running app within container, the localhost is the container itself. It will not be able (by default) to reach other apps with calls like ```curl http://localhost:5000/api/healthcheck```.

Caveat:
While using web frameworks that distinguish server-side and client-side rendering, we need to be extra careful. Localhost for server-side rendering is the VM/container app runs on. Localhost on client-side rendered code is the machine of end user (laptop/tablet/smartphone). This is common cause for errors when calling backend api endpoints from frontend.



## General Docker notes

```bash
docker run -p 80:80 <myimage>     # port linking
docker run -it -p 80:80 <myimage>   # runs interactively (we can see logs rolling)
docker run -d -p 80:80 <myimage>   # spins up container in background
docker run -d --name <mycontainer> -p 80:80 <myimage>   # assign custom name to container

docker ps   # shows running containers
docker ps -a  # shows all containers

docker stop <mycontainer>
docker kill <mycontainer>

docker inspect <mycontainer> # shows detailed info about container (running/stopped)

docker stats   # resource usage for all cotainers
docker top <mycontainer>  # show running processes inside container

docker network ls # shows docker networks

# docker logging:
docker logs -f <mycontainer>   # equivalent of tail -f on the container logs
```

Troubleshooting commands
```bash
docker attach <mycontainer> # do not use, will likely cause container outage, takes over main shell that runs the actual app
docker exec <mycontainer> whoami  # execute command within container
docker exec -it <mycontainer> /bin/bash    # favourite t-shooting command

docker images
docker rmi <image_name>

docker system prune # removed hanging images and residual stopped containers (can clean up lots of disk space, relatively safe command), some admins run the command from cron daily
```




# Docker security

Docker does not provide the same sandboxing as regular VM does.
Docker daemon is just a process running inside VM and Docker is managed by VM kernel.
Docker daemon typically runs under root user (from VM perspective) and users that have access to Docker daemon are typically members of ```docker``` group. Making them essentially system admins -> access to ```docker``` group needs to be limited. From security standpoint, do not treat containers as micro-VMs.

Docker engine generates several linux namespaces, such as: process ID (PID), mount (MNT), networking (NET), USER namespace, ...
Linux namespaces are meant for isolation purposes.

"Best" security docker practices:

- keep docker engine patched regularly
- securing docker socket (```/var/run/docker.sock```) only accessible by root and users in ```docker``` group (sysadmins, not devs)
- docker does not fix bad/insecure app code
- always set unprivileged user (add user to Dockerfile)
- when running Docker, use ``--user``` flag to docker run command
- set nologin for root user in container
- download only official images from container repos (such as DockerHub)
- start docker container with ```no-new-privileges``` to avoid rights escalation
- mount files to container in read only where feasible (`--mount source=<...>,readonly`)
- run whole container in read only where feasible ```docker run --read-only <myimage> sh -c 'echo "Testing" > /tmp/test'```
- do not include passwords, API keys, RSA keys into Dockerfile/image
- read a book on Docker security `:)`
- ```COPY . .``` command is recursive, you can unknowingly copy sensitive data to image, make sure you use `.dockerignore` file to limit what we copy to image
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

## AppArmor

Additional security layer for containers

documentation for Ubuntu
https://ubuntu.com/server/docs/security-apparmor

It is regular apt package
```bash
sudo apt install apparmor-profiles
```

from docker docs:
https://docs.docker.com/engine/security/apparmor/

AppArmor security profiles for Docker:

AppArmor (Application Armor) is a Linux security module that protects an operating system and its applications from security threats. To use it, a system administrator associates an AppArmor security profile with each program. Docker expects to find an AppArmor policy loaded and enforced.

Docker automatically generates and loads a default profile for containers named docker-default. The Docker binary generates this profile in tmpfs and then loads it into the kernel.

Note:
This profile is used on containers, not on the Docker daemon.

example how to run hardened container secured with AppArmor:

```bash
docker run --rm -it --security-opt apparmor=docker-default hello-world
```

```bash
coil@devVM:~/Desktop/DevOpsLab$ sudo apparmor_status
[sudo] password for coil: 
apparmor module is loaded.
47 profiles are loaded.
42 profiles are in enforce mode.
   ...
   docker-default                   <--  OUR DEFAULT DOCKER PROFILE in ENFORCE MODE
   libreoffice-senddoc
   libreoffice-soffice//gpg
   libreoffice-xpdfimport
   lsb_release
   man_filter
   man_groff
   nvidia_modprobe
   ...
5 profiles are in complain mode.
   /usr/sbin/sssd
   libreoffice-oosplash
   libreoffice-soffice
   snap.code.code
   snap.code.url-handler
0 profiles are in kill mode.
0 profiles are in unconfined mode.
19 processes have profiles defined.
2 processes are in enforce mode.
...
17 processes are in complain mode.
...
   /usr/bin/bash (...) snap.code.code
   /usr/bin/bash (...) snap.code.code
   /usr/bin/bash (...) snap.code.code
...
0 processes are unconfined but have a profile defined.
0 processes are in mixed mode.
0 processes are in kill mode.
coil@devVM:~/Desktop/DevOpsLab$ docker run --rm -it --security-opt apparmor=docker-default hello-world
...
Status: Downloaded newer image for hello-world:latest
...
Hello from Docker!
...
coil@devVM:~/Desktop/DevOpsLab$ 
```

Useful AppArmor links:
- https://docs.docker.com/engine/security/apparmor/
- https://dockerlabs.collabnix.com/advanced/security/apparmor/
- https://security.padok.fr/en/blog/security-docker-apparmor
- https://test-dockerrr.readthedocs.io/en/latest/security/apparmor/
- https://gcore.com/learning/advanced-docker-security-with-apparmor/



## Image Security Scanning

Login to your DockerHub account, use your access token.

Our example image with security scan:
https://hub.docker.com/repository/docker/swilab/backend-img/general


```bash
docker login -u swilab

cd <somedir w dockerfile>
docker build -t swilab/backend-img .
docker push swilab/backend-img

# paid feature - static scanning on DockerHub
# docker scan swilab/backend-img:latest
```

Static image scanning with 'Snyk' is paid feature on DockerHub.

New Docker Scout vulnerability scan is free for 3 DockerHub repos.

Our lab image security scan is available via DockerHub GUI:
https://scout.docker.com/reports/org/swilab/vulnerabilities?stream=latest-indexed

Links
- https://docs.docker.com/scout/
- https://github.com/docker/scout-cli



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

Port mapping:

We can run app on its default port in container and expose it on VM on different port.
So for example flask runs by default on port 5000, so the mapping would be ```-p 5001:5000```.

But since building Docker images takes time, it would delay us in the development.
Especially React/NextJS frontend image builds are heavy on resources, especially when we use Linux running in Virtual box as dev machine. You will see lots of Disk IO wait times and system interrupts during builds.


So, turns out it is convenient to have apps running locally during dev on the same port that container would be using. On main dev VM, there would also be NGINX reverse proxy aware of the app/container ports.

Lets say we have frontend on port 3000, flask backend on 5000 and express backend on 5000

Then we would remap the apps themselves to ports corresponding to final container setup and let revese proxy to be aware of the port architecture.
So it would be 3000, 5100 and 5200. This way we can run dev tests easily without containers and we save lots of time.

So basically, app architecture should be the same with and without containers. You can let app know it runs within container with injected env vars.



## Other useful Docker commands

```bash
docker ps -a                    # list all containers (even stopped and paused ones)
docker pause <mycontainer>      # pauses container
docker unpause <mycontainer>    # unpauses container
docker restart <mycontainer>    # restarts container
docker stop <mycontainer>       # stops container
docker start <mycontainer>      # starts contaner
docker stop -t 10 <mycontainer> # stops gracefully (SIGTERM), force stop later if need be (SIGKILL)
docker kill <mycontainer>       # force stop container
docker logs <mycontainer>       # shows logging for containers
```

## Image and Docker hub related commands

```bash
docker login -u <dockerhub_account>
docker image ls  # (docker images)
# create your Dockerfile and then in the same directory run:
docker image build --tag dockerhubuser/myimage:v0.1
# alternatively
docker build -t myimage:v0.1
# then push to DockerHub repo if needed
docker push <dockerhubuser>/myimage:v0.1

# pull our image from registry if needed
docker pull <dockerhubuser>/myimage:v0.1

#remove the image locally
docker image rmi <dockerhubuser>/myimage:v0.1
# alternatively
docker rmi <dockerhubuser>/myimage:v0.1
```

## Docker volumes for persistence
3 types: `host`, `anonymous` and `named volumes` (use named volumes for production ideally)

#### Host volumes (`-v hostVM:<container>`)

```docker run -v /home/mount/data:/var/lib/mysql/data --name <container> <image>```

#### Anonymous Volumes (`-v </container/dir>`)
```docker run -v /var/lib/mysql/data --name <container> <image>```
some random hash volume will be created under ```/var/lib/docker/volumes/``` directory on host VM

#### Named volumes (```-v <name>:</container/dir>```) 
need to create docker volume first

```bash
docker volume create volume_1
docker volume ls
docker volume inspect volume_1
docker run -v <vol_name>:/var/lib/mysql/data --name <container> <image>
docker volume rm volume_1 # remove volume when not needed
docker volume ls
```

Named volumes work well with docker-compose files, easy to define shared dir for containers (for example for logging)



# Kubernetes (general notes) - DRAFT

kubernetes is state machine


pods are dynamic, but services are static, services have static IP address - serves as load balancer for pods/containers

node port service exposes Ips of worker nodes, not really good practice
LoadBalancer service is much better, but this is for cloud providers

not sure how to actually do it on VM


ingress just needs one cloud load balancer, so it is much cheaper
instructor always always goes for ingress (like nginx, traefik)



also minikube has ingress with one simple command (builtin nginx ingress)





