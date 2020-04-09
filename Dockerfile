FROM python:3.8.2

WORKDIR /sahabee/
COPY requirements-pip.txt /tmp/
RUN pip install -r /tmp/requirements-pip.txt && rm /tmp/requirements-pip.txt
COPY . .
RUN python manage.py collectstatic --no-input
RUN chmod +x run.sh

CMD ./run.sh