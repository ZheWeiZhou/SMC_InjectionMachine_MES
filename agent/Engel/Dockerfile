FROM python:3.10-slim

RUN apt-get -yqq update; apt-get -yqq install curl

COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

COPY ./Engelagent.py /workspace/Engelagent.py
COPY ./healthcheck.sh /workspace/healthcheck.sh

WORKDIR /workspace


HEALTHCHECK --interval=10s CMD ["/healthcheck.sh"]

CMD ["python", "Engelagent.py"]