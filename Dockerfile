
FROM python:3.12


WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV FLASK_APP=api.log_route.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "run.py"]