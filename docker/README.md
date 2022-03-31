This folder contains a docker environment for developing KubOS. 

It consists of a docker container and a docker compose config to make the experience as similar as possible to "vagrant up".

to build the container run `docker build -t kubos-dev .`

to get a shell into the container, use `docker-compose run --rm kubos-dev`

The docker container will auto-mount your current directory inside /vagrant just like the KubOS SDK does. To use a different directory, either change the docker-compose file or build the container, then move the docker-compose file to the location you want to mount and treat it the same as you would your `Vagrantfile` 
