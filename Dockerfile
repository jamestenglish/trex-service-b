FROM python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
EXPOSE 8080
ADD . /code
WORKDIR /code
RUN mkdir /code/results
CMD ["python", "app.py"]
