FROM python:3.10-slim

WORKDIR /pj-userservice

COPY requirements.txt /pj-userservice/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pj-userservice/requirements.txt

COPY . /pj-userservice/src

WORKDIR /pj-userservice/src

# ARG MONGO_URI="mongodb://host.docker.internal:27017/"
# ARG MONGO_DB_NAME="UserService"
# ARG DISCORD_WEBHOOK="https://discord.com/api/webhooks/1050321482401726484/7Gu-WmY0P_0m5d1mA3FjCsFIXQL5AW2izzXXWoemqHvNRoD5D1ppEb48wuFBsCqAAm9t"
# ARG BASE_PATH="/service/user"
# ARG BASE_PATH_CLASSES="/service/classes"
# ARG VERSION_1="/v1"
# ARG FE_URL="http://localhost:3000"

# ENV MONGO_URI=${MONGO_URI}
# ENV MONGO_DB_NAME=${MONGO_DB_NAME}
# ENV DISCORD_WEBHOOK=${DISCORD_WEBHOOK}
# ENV BASE_PATH=${BASE_PATH}
# ENV BASE_PATH_CLASSES=${BASE_PATH_CLASSES}
# ENV VERSION_1=${VERSION_1}
# ENV FE_URL=${FE_URL}

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]