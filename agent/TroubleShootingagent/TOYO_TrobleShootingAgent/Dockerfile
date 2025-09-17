FROM python:3.10-slim

RUN apt-get -yqq update; apt-get -yqq install curl

COPY ./requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/requirements.txt

COPY ./TOYOtroubleshootagent.py /workspace/TOYOtroubleshootagent.py
COPY ./TOYO_dataprocess_function.py /workspace/TOYO_dataprocess_function.py
COPY ./healthcheck.sh /workspace/healthcheck.sh
RUN chmod +x /workspace/healthcheck.sh
WORKDIR /workspace


HEALTHCHECK --interval=10s CMD ["/workspace/healthcheck.sh"]

CMD ["python", "TOYOtroubleshootagent.py"]