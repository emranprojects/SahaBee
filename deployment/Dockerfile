FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip python3-dev software-properties-common sshpass curl
RUN pip3 install --upgrade pip==20.0.2
RUN pip install ansible==2.9.0
RUN ssh-keygen -t rsa -b 4096 -N '' -C "deployment-docker@CI" -f '/root/.ssh/id_rsa'