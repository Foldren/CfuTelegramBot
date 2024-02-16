FROM python:3.12-alpine
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install pydantic==2.6.1 --force-reinstall
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./source .
CMD ["python", "bot.py"]
