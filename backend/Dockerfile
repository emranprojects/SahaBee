FROM python:3.8.6-alpine

WORKDIR /sahabee/
COPY requirements-apt.txt /tmp/
RUN apk update && cat /tmp/requirements-apt.txt | xargs apk add
COPY requirements-pip.txt /tmp/
RUN pip install -r /tmp/requirements-pip.txt && rm /tmp/requirements-pip.txt
COPY . .
RUN chmod 444 ./timesheet-template.xlsx
RUN python manage.py collectstatic --no-input
RUN chmod +x run.sh

CMD ./run.sh