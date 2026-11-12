FROM python:3.12-slim

RUN useradd --create-home flask
WORKDIR /home/flask

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=flask:flask app.py test.py ./

ENV FLASK_APP=app.py
EXPOSE 5000

USER flask
CMD ["python", "app.py"]
