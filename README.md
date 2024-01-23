## ASSUMPTIONS

This build server application assumes that:

- all related C program files are packaged into an expected structure (i.e. files are contained within a directory whose name is the same as the prefix of the target file, and the directory is contained within a zip file whose prefix is the same as directory's name). 

    **NOTE**: Application will automatically skip over (and locally remove from build server) any invalid zip packages, well as any other unexpected files that may randomly exist in targeted Git repo.

- at most 1 instance of application in on-demand mode and 1 instance of application in auto mode is required to be able to run concurrently with each other.

    **NOTE**: User will be notified if another instance is already running in same mode and application will exit.

    **NOTE**: If an instance in one mode is started during the build cycle of the other mode, the instance will wait until the build cycle of the other instance is complete before beginning its own build cycle (excluding the period of time between build cycles that occur in auto mode).

- records shall be automatically removed for any build attempts that were not fully completed due to an unexpected runtime error or user-signaled exit (as opposed to, for example, being left in place with an updated status of INCOMPLETE and obscuring records for fully completed build attempts).

## ALL-IN-ONE SCRIPT

To automatically set up virtual environment, build and run Docker image as container, deploy and initialize MySQL database, start Flask web server, and run build server with default settings.

***WARNING***: This script removes all pre-existing Docker objects, including volumes.

    sh deploy-buildserver.sh

## BUILD SERVER CONTAINER

To manually build Docker image:

> docker compose build `<container service name>`

e.g.

    docker compose build buildserver_svc

To manually create and start Docker container:

> docker compose run -p `<src port>`:`<dst port>` `<container service name>`

e.g.

    docker compose run -p 5000:5000 buildserver_svc

-- OR --

> docker run -p `<src port>`:`<dst port>` -e MYSQL_ROOT_PASSWORD='`<password>`' `<image name>:<image tag>` 

e.g.

    docker run -p 5000:5000 -e MYSQL_ROOT_PASSWORD='D3v0p$2' buildserver_img:latest 

To log into running container:

    docker exec -it <container hash> bash

## BUILD SERVER DATABASE (DB)

To log into MySQL from within container and initialize database:

> mysql -u root -p'`<password>`' -P `<port>` -h `<ip>` < "../`<database init script>`.sql"

e.g.

    mysql -u root -p'D3v0p$2' -P 3306 -h 0.0.0.0 < "../buildserver-init-db.sql"

## BUILD SERVER WEB PAGE (GUI)

To manually start Flask app:

> exec gunicorn -w 1 --timeout 200 --bind `<ip>`:`<port>` `<module name>`:`<container/app name>`

e.g.

    exec gunicorn -w 1 --timeout 200 --bind 127.0.0.1:5000 buildserver_mod:buildserver_con

## BUILD SERVER APPLICATION (BIZ)

To start build server application in on-demand mode (w/ default url and interval):

    python -u buildserver_mod.py --mode o

To start build server application in auto mode (w/ default url and interval):

    python -u buildserver_mod.py --mode a

To start build server application with a given interval (w/ default mode and url):

    python -u buildserver_mod.py --interval 300

To specify a .git or .zip URL (w/ default mode and interval):

> python -u buildserver_mod.py --url `<URL>`

e.g.
```
python -u buildserver_mod.py --url https://github.com/jsandreyo/repo_b.git
```
```
python -u buildserver_mod.py --url https://github.com/jsandreyo/repo_b/hello1.zip
```

**Auto Mode**: will process a given or assumed remote Git resource every x number of seconds.

**On-Demand Mode**: will process a given or assumed remote Git resource one time through.

**NOTE**: Both modes can be used in combination with any qualified Git URL ending in either .git or .zip.

## DEFAULT VALUES

**NOTE**:

- Auto mode is default build cycle mode.  To reconfigure this default value, edit global **DEFAULT_BUILD_CYCLE_MODE** constant in **g_.py**.

- https://github.com/jsandreyo/repo_b.git is default remote Git resource.  To reconfigure this default value, edit global **DEFAULT_GIT_REPO_URL** constant in **g_.py**.

- 180 seconds (3 minutes) is default interval for continuous build cycles.  To reconfigure this default value, edit global **DEFAULT_INTERVAL_SECONDS** constant in **g_.py**


##

Author: John Andreyo \
Copyright: Copyright (c) 2024. All rights reserved. \
License: Please see LICENSE file in project's root. \
Version: 2.0
