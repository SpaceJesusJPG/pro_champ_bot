FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY . .
CMD ["python", "pro_champ_bot.py"]