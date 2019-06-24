FROM python:3-alpine

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY exporter.py /usr/local/bin/
RUN chmod 555 /usr/local/bin/exporter.py
EXPOSE 3001

RUN adduser -S gitlab_monitor

VOLUME /home/gitlab_monitor/.python-gitlab.cfg
USER gitlab_monitor
CMD /usr/local/bin/exporter.py
