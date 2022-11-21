FROM python:3.10-slim

WORKDIR /pj-userservice

COPY requirements.txt /pj-userservice/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pj-userservice/requirements.txt

COPY . /pj-userservice/src

WORKDIR /pj-userservice/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]