######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

### IMAGE BUILD SCRIPT ###

#!/bin/bash

# *** Only need to run this block once locally ***
# ensure sufficient permissions in order to execute python
#sudo chown -R $(id -u):$(id -g) $HOME/.docker
#sudo chmod +rwx -R $HOME/.docker

read -p "
************************************** WARNING: DATA LOSS RISK! *************************************
Any and all pre/existing Docker objects generated by this project will be removed, including volumes.
************************************** WARNING: DATA LOSS RISK! *************************************

Are you sure you want to continue? (y/n): " answer
case $answer in
    y|Y)
		container_name=buildserver_con_2.1
	    echo "BUILD SERVER (local): Shutting down and removing container (and volume) originating from the run_demo.sh script's 'Docker run' command..."
		if [ ! "$(docker ps -q -f name=$container_name)" ]; then # if not running
			if [ $( docker ps -a -f name=$container_name | wc -l ) -eq 2 ]; then # if exists
				docker rm -v $container_name
			fi
		else # if running (exists)
			docker stop $container_name && docker rm -v $container_name
		fi
        
        echo "BUILD SERVER (local): Removing images originating from this script's 'Docker compose build' command..."
        generic_image_and_tag_name=buildserver_img:latest
        docker rmi --force $(docker images --format "{{.Repository}}:{{.Tag}}" $generic_image_and_tag_name -a -q)
        dockerhub_image_and_tag_name=jsandreyo/buildserver:2.1
        docker rmi --force $(docker images --format "{{.Repository}}:{{.Tag}}" $dockerhub_image_and_tag_name -a -q)
        ;;
    n|N)
        echo "Script canceled. Will now exit."
        exit
        ;;
    *)
        echo "Invalid answer. Will now exit."
        exit
        ;;
esac

# *** Only need to run this block once locally ***
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

# Build image
echo "BUILD SERVER (local): Rebuilding image..."
docker compose build buildserver_svc

# Locally copy and rename image in preparation for upload to DockerHub
docker tag buildserver_img:latest jsandreyo/buildserver:2.1
