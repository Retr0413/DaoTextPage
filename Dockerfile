FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nginx \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=8080 

EXPOSE 8080

CMD ["sh", "-c", "nginx -g 'daemon off;' & flask run --host=0.0.0.0 --port=$PORT"]
