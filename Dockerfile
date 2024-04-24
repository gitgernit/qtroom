FROM python:3.12

WORKDIR /
COPY . .
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements/server.txt
CMD ["python", "server/main.py"]
