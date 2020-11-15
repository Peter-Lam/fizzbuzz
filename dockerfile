FROM python
ENV DOCKER=true
ENV TZ=America/Toronto
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
CMD tail -f /dev/null