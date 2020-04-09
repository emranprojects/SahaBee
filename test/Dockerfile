FROM python:3.8.2
COPY requirements-pip.txt /tmp/
RUN pip install -r /tmp/requirements-pip.txt && rm /tmp/requirements-pip.txt
ENTRYPOINT [ "/usr/local/bin/pytest" ]