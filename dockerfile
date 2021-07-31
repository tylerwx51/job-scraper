FROM python:3

WORKDIR /code

COPY code/ .
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]