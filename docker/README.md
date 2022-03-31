This folder contains a docker environment for developing KubOS. 

It consists of a docker container and a docker compose config to make the experience as similar as possible to "vagrant up".

to build the container run `docker build -t kubos-dev .`

to get a shell into the container, use `docker-compose run --rm kubos-dev`