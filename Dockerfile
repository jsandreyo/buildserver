######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

FROM mysql:8.0.35

# Copy application files from project to container
WORKDIR /app
COPY . /app

RUN echo "BUILD SERVER (remote): Installing general dependencies..." \
&& rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2023 \
&& microdnf -y clean all \
&& microdnf -y install --setopt=install_weak_deps=0 python38 \
&& microdnf -y install --setopt=install_weak_deps=0 git-all \
&& microdnf -y install --setopt=install_weak_deps=0 make \
&& microdnf -y install --setopt=install_weak_deps=0 gcc \
&& microdnf -y install --setopt=install_weak_deps=0 wget

RUN echo "BUILD SERVER (remote): Refreshing virtual environment..." \
######### Set up virtual environment for remote container #########
# Clean virtual environment
&& rm -rf /app/.venv \
# Regenerate virtual environment
&& python3 -m venv /app/.venv \
# Add virtual environment to Path
&& export PATH="/app/.venv/bin:$PATH" \
# Activate virtual environment
&& . /app/.venv/bin/activate

# Install pip requirements
RUN echo "BUILD SERVER (remote): Installing pip dependencies..." \
&& python3 -m pip install -r /app/requirements.txt

# Enable writing to zip error log file (remote)
RUN chown -R mysql:mysql /app/error-logs \
&& chmod +rwx -R /app/error-logs \
# Enable writing to web output log file (remote)
&& chown -R mysql:mysql /app/output-logs \
&& chmod +rwx -R /app/output-logs

# Enable writing to c programs zip directory and make safe for git (remote)
RUN chown -R mysql:mysql /app/c_programs_zip \
&& chmod +rwx -R /app/c_programs_zip \
&& git config --global --add safe.directory "*" \
# Enable writing to c programs src directory (remote)
&& chown -R mysql:mysql /app/c_programs_src \
&& chmod +rwx -R /app/c_programs_src

# Copy entrypoint directory and script(s) to designated location
RUN chmod +rwx -R /docker-entrypoint-initdb.d \
&& mv /app/docker-entrypoint-initdb.d / -f

# Configure Flask environment ("development" implies debug True)
ENV FLASK_ENV=development
#ENV FLASK_DEBUG=True

# Configure Flask application (currently executed from init script)
#ENV FLASK_APP=${workspaceRoot}/buildserver_mod.py

# Keeps Python from generating .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=True
# Turns off buffering for easier container logging.
ENV PYTHONUNBUFFERED=True
