######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

#!/bin/sh

echo "BUILD SERVER (remote): Changing to app directory..."
cd ../app

echo "BUILD SERVER (remote): Sleeping for 20s..."
sleep 20

echo "BUILD SERVER (remote): Initializing up database..."
mysql -u root -p'D3v0p$2'< "buildserver-init-db.sql"

dashed_line='--------------------------------------------------------------------------------------------------------------------------------------'

set -m
echo "BUILD SERVER (remote): Running Flask app in background and Python instances in foreground..."
echo $dashed_line
echo $dashed_line
echo "Starting Demo Part 1: pull a single C program from GitHub repo A and build/register, but don't monitor program for subsequent changes."
echo $dashed_line
echo $dashed_line
# <python module name>:<container name / name of Flask instance created within python module>
exec gunicorn -w 1 --timeout 200 --bind :5000 buildserver_mod:buildserver_con > /dev/null \
& python3 -u buildserver_mod.py --mode o --url https://github.com/jsandreyo/repo_a/raw/main/hello8.zip \
&& echo $dashed_line \
&& echo $dashed_line \
&& sleep 5 \
&& echo "Starting Demo Part 2: pull multiple C program's from GitHub repo B and build/register, then monitor repository for subsequent changes." \
&& echo $dashed_line \
&& echo $dashed_line \
&& python3 -u buildserver_mod.py --interval 30 && fg
