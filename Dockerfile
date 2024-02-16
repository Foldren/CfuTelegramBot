FROM python:3.12-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY ./source .
CMD ["python", "bot.py"]
