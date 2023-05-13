# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]