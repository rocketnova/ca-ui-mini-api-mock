FROM python:alpine
RUN apk update \
  && pip install falcon
COPY mock.py /srv/mock.py
# Run python unbuffered to view print lines in docker logs
CMD python -u /srv/mock.py
