FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y nodejs npm

RUN pip install Flask
RUN npm install -g prettier@3.4.2

CMD ["python", "main.py"]
