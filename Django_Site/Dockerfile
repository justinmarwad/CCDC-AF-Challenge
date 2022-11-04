FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY AF_Material /AF_Material 

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY AF /code/

COPY entrypoint.sh /
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
