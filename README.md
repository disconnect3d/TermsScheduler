# TermsScheduler
TermsScheduler is a web application that lets students sign up for subjects and particular terms.


### It consists of three parts:

* Frontend made in AngularJS
* Backend - REST Api made in Flask
* Ant colony optimization algorithm written in C and scripted in Perl (this part *might* get rewritten because it is old and not so maintainable) - TBD (*not yet added to the repo*)


### Launching

For more info on specific subproject (frontend/backend) see README files in frontend/backend directories.

However, if you want just to check out/test project, it can be run through [docker-compose](https://docs.docker.com/compose/)
(if you are not into topic of, check out [Docker](https://www.docker.com/what-docker) first):

```bash
$ docker-compose build && docker-compose up
```

This will launch two containers - one for backend and one for frontend.

The backend container will be exposed to port 5000 and the frontend one to 8282 (configured in *docker-compose.yml*).

**IMPORTANT NOTE: Currently, the docker containers use debug settings, so don't use it for deployment.**


The backend part has been written for a university course "Advanced Web Technologies" at AGH University of Science and Technology.
