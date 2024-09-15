# docker-crow-svelte-hello-world
An example project to deploy a Crow + Svelte application using Docker


WIP

docker run --rm --name=svelte-docker -p 5000:80 svelte-docker
cd svelte-app
docker build . -t svelte-docker
