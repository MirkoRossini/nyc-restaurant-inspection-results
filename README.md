# docker-crow-svelte-hello-world
An example project to deploy a Crow + Svelte application using Docker Compose.


We define two Docker containers:

  * A Svelte + nginx component
  * A Crow application component


The Svelte application is built using the static adapter.
The generated files are then copied into a nginx container.

The nginx container is also configured to proxy calls 
to /app to the Crow app (see svelte-app/nginx.conf).

The crow-app container downloads a Crow release, unpacks it
and installs it in an ubuntu container. Another container
is used to run the application.


simply call docker-compose up to run the setup.


