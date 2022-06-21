FROM python:3.9
WORKDIR /code
COPY requirements.txt .
COPY src/ .
RUN pip install -r requirements.txt
CMD [ "python3", "src/main.py" ]