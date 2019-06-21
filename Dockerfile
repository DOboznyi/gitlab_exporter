FROM ubuntu:18.04
COPY . /
RUN pip install -r requirements.txt
CMD python merge_requests.py
