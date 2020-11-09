FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip python3-dev software-properties-common sshpass curl
RUN pip3 install --upgrade pip==20.2.4
RUN pip install ansible==2.10.0
RUN ansible-galaxy collection install community.general