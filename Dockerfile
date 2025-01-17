FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 libmariadb-dev gcc pkg-config
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
