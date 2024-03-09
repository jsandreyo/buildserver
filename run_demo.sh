######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

#!/bin/bash

sub_tmp_dir_path=
function cleanup(){
	echo "Removing host browser pipe..."
  trap - EXIT
  if [ -n "$sub_tmp_dir_path" ] ; then rm -rf "$sub_tmp_dir_path"; fi
  if [ -n "$1" ]; then trap - $1; kill -$1 $$; fi
}
trap 'cleanup' EXIT

function print_err_line_num(){
    echo "An error occurred on line $1"
    exit 1
}
trap 'print_err_line_num $LINENO' ERR

echo "
*************************
*** BUILD SERVER DEMO ***
*************************
by John Andreyo
Version 2.1
Copyright (c) 2024"

read -p "
This script will pull down the image for the build server from DockerHub (if it does not yet exist locally), \
run it as a container, and then commence a demonstration of it.  It will first remove any containers it previously \
spawned, and assumes you minimally have Docker and a web browser installed on your Linux-based O/S, \
as well as access to the Internet on the host machine.

Would you like to continue? (y/n): " answer1

port=0

case $answer1 in
    y|Y)
		while true; do
			read -p "
Please enter a 5000 based port number for this application's web page to run on: " input

			if ! [[ "$input" =~ ^[5][0-9]{3}$ ]]; then
				echo "$input is not a valid port number."
				continue;
			else
				read -p "
*********************** WARNING: DATA LOSS RISK! *****************************
An attempt will be made to first halt any processes associated with this port.
*********************** WARNING: DATA LOSS RISK! *****************************

Would you like to continue using the specified port of $input? (y/n/x): " answer2

				case $answer2 in
					y|Y)
						port=$input
						break
						;;
					n|N)
						echo "Entry canceled. Please try again."
						continue
						;;
					x|X)
						echo "Demo canceled. Will now exit."
						exit
						;;
					*)
						echo "Invalid answer. Please try again."
						continue
						;;
				esac
			fi
		done

		#export DISPLAY=:0

		set -m	

		read -p "
********************** WARNING: DATA LOSS RISK! ****************************
Any container and volume previously spawned by this script will be removed.
********************** WARNING: DATA LOSS RISK! ****************************

Would you like to continue? (y/n): " answer
		case $answer in
			y|Y)
				container_name=buildserver_con_2.1
				echo "Shutting down and removing container (and volume) originating from this script's 'Docker run' command..."
				if [ ! "$(docker ps -q -f name=$container_name)" ]; then # if not running
					if [ $( docker ps -a -f name=$container_name | wc -l ) -eq 2 ]; then # if exists
						docker rm -v $container_name
					fi
				else # if running (exists)
					docker stop $container_name && docker rm -v $container_name
				fi
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

		echo "Killing any processes using user-specified port..."
        sudo kill -9 $(sudo lsof -t -i:$port) 2> /dev/null || true # toss usage info and ignore err if no process is using port

		echo "Creating host browser pipe..."
		pipe_name=hostbrowserpipe
		sub_tmp_dir_path=$(mktemp -d)
		named_pipe_file_path="$sub_tmp_dir_path/$pipe_name"
		mkfifo $named_pipe_file_path
		echo "File path to host browser pipe is: " $named_pipe_file_path

		echo "Checking if expected docker image exists locally. If not, image will be downloaded from DockerHub..."
		dockerhub_image_and_tag_name=jsandreyo/buildserver:2.1
		if ! docker image inspect $dockerhub_image_and_tag_name >/dev/null 2>&1; then
			echo '**********************************************************************************' 
			echo '**********************************************************************************' 
			echo "Image does not exist locally. Will now attempt to download image from DockerHub..."
			echo '**********************************************************************************' 
			echo '**********************************************************************************' 
			docker pull $dockerhub_image_and_tag_name
			echo Done!
		fi

		# run image called jsandreyo/buildserver:2.1 as a container called buildserver_con_2.1 with a named pipe binding
		# (for invoking host browser from within container) and a user-specified port binding (for exposing port used
		# to run application's web page inside container, to host).
		echo "Spinning up build server container and initializing MySQL Server..."
		docker run --name $container_name -v $named_pipe_file_path:"/var/run/$pipe_name" -p $port:$port -e MYSQL_ROOT_PASSWORD='D3v0p$2' $dockerhub_image_and_tag_name &

		# make named pipe continually listen for any URL's echoed within container
		echo "Waiting for container to spawn Flask instance and browser to open..."
		while read -r URL < $named_pipe_file_path; do xdg-open "$URL"; done &

		# as a separate process, execute local demo script from within running container called buildserver_con_2.1, passing in user-specified port binding
        echo "Executing demo script within container..."
		gnome-terminal --geometry 117x19 -- bash -c "docker exec -e PORT=$port -i $container_name sh < container-demo-script.sh; exec bash" && fg
        ;;
    n|N)
        echo "Demo canceled."
        ;;
    *)
        echo "Invalid answer. Please try again."
        ;;
esac

kill -9 $PPID
