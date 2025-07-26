FROM python:3.13.5-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /home/appuser/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /home/appuser/app

EXPOSE 8000

CMD ["fastapi", "dev", "main.py"]
