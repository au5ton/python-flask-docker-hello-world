FROM python:3.9-bullseye
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install python3-opencv  -y
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
