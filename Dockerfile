FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY clean_csv.py .
COPY skill-assessment-202511.csv .

CMD ["python", "clean_csv.py"]
