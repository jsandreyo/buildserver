######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

### DEPLOYMENT SCRIPT ###

#!/bin/bash

# ensure sufficient permissions in order to execute python
#sudo chown -R $(id -u):$(id -g) $HOME/.docker
#sudo chmod +rwx -R $HOME/.docker

echo "BUILD SERVER (local): Shutting down previous Container..."
echo "BUILD SERVER (local): - Removing previous Docker compose objects..."
docker compose down --remove-orphans --volumes
echo "BUILD SERVER (local): - Removing previous Docker build objects..."
docker system prune --force --all --volumes

# echo "BUILD SERVER (local): Installing general dependencies..."
# sudo apt-get -y update && sudo apt-get -y upgrade && sudo apt-get -y clean all
# sudo apt-get -y install python38
# sudo apt-get -y install git-all
# sudo apt-get -y install make
# sudo apt-get -y install gcc
# sudo apt-get -y install wget

echo "BUILD SERVER (local): Re/creating clean local temp file directories..."
dir1=c_programs_src
if [ -d "$dir1" ]; then rm -rf $dir1/*; else mkdir $dir1; fi
dir2=c_programs_zip
if [ -d "$dir2" ]; then rm -rf $dir2/*; else mkdir $dir2; fi

echo "BUILD SERVER (local): Re/creating clean local log file directories..."
dir3=error-logs
if [ -d "$dir3" ]; then rm -rf $dir3/*; else mkdir $dir3; fi
dir4=output-logs
if [ -d "$dir4" ]; then rm -rf $dir4/*; else mkdir $dir4; fi

echo "BUILD SERVER (local): Refreshing virtual environment..."
# Clean virtual environment
rm -rf .venv
# Regenerate virtual environment
python3 -m venv .venv
# Add virtual environment to Path
export PATH="/.venv/bin:$PATH"
# Activate virtual environment
. .venv/bin/activate

# Install pip requirements
echo "BUILD SERVER (local): Installing pip dependencies..."
python3 -m pip install -r requirements.txt

# Build image, re/create and start container (port mapping should match Flask port)
echo "BUILD SERVER (local): Rebuilding image and spinning up container..."
docker compose build buildserver_svc
docker compose run -p 5000:5000 buildserver_svc
