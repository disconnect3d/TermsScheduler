# TermsScheduler
TermsScheduler is a web application that lets students sign up for subjects and particular terms.


### It consists of three parts:

* Frontend made in AngularJS
* Backend - REST Api made in Flask
* Ant colony optimization algorithm written in C and scripted in Perl (this part *might* get rewritten because it is old and not so maintainable) - TBD (*not yet added to the repo*)

For more info on specific subproject (frontend/backend) see README files in frontend/backend directories.

### Launching

The project can be run through [docker-compose](https://docs.docker.com/compose/)
(if you are not into topic of, check out [Docker](https://www.docker.com/what-docker) first):

```bash
$ docker-compose build && docker-compose up
```

This will build two docker images (install all dependencies to the images, not in your system) and then run containers based on built images.

The containers will expose ports to the host OS:

- 5000 - for backend
- 8282 - for frontend

So both parts can be accessed from localhost.

The exposed ports can be changed in the *docker-compose.yml* file.

**IMPORTANT NOTE: Currently, the docker containers use debug settings, so don't use it for deployment.**


### Authors

* backend - [Dominik Czarnota](https://github.com/disconnect3d/)
* frontend - [Aleksander Kawala](https://github.com/Alexander3/)

The backend part has been written for a university course "Advanced Web Technologies" at AGH University of Science and Technology.
