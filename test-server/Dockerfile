FROM python:3.8-slim 
WORKDIR /
COPY requirements.txt ./
COPY /app ./app

RUN pip install -r requirements.txt \
	&& rm requirements.txt 


CMD ["python", "./app/main.py"]

