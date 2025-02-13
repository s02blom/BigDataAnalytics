FROM python:3.10-slim

WORKDIR /monitoring

RUN apt update
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE $FLASK_RUN_PORT

ENTRYPOINT ["flask", "--app", "monitoring", "run", "--debug"]
# ENTRYPOINT ["flask", "--app", "monitoring", "run", "--debug", "--no-reload"]  For avoiding the double restarts of flask in the beginning