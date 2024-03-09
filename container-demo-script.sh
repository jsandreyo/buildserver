######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

#!/bin/sh

line_sep='_____________________________________________________________________'

echo "Waiting for MySQL Server to initialize before starting build server demo..."

while ! mysqladmin ping -h 0.0.0.0 --silent; do
    sleep 1
done

set -m
echo "BUILD SERVER (remote): Running Flask app in background and Python instances in foreground..."
# <python module name>:<container name / name of Flask instance created within python module>
exec gunicorn -w 1 --timeout 200 --bind :$PORT buildserver_mod:buildserver_con > /dev/null \
& echo http://localhost:$PORT >> /var/run/hostbrowserpipe \
&& echo "Waiting for browser to open before running build server use cases..." && sleep 13 \
&& echo $line_sep \
&& echo "" \
&& echo "Starting Demo Part 1: pull a single C program from GitHub repo A
and build/register, but don't monitor program for subsequent changes." \
&& echo $line_sep \
&& python3 -u buildserver_mod.py --mode o --url https://github.com/jsandreyo/repo_a/raw/main/hello8.zip \
&& sleep 5 \
&& echo $line_sep \
&& echo "" \
&& echo "Starting Demo Part 2: pull multiple C program's from GitHub repo B
and build/register, then monitor repository for subsequent changes." \
&& echo $line_sep \
&& python3 -u buildserver_mod.py --interval 30 && fg
