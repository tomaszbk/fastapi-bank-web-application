FROM python:3.11.6
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
#when building image
RUN pip install --no-cache-dir -r requirements.txt 
COPY . .
#when container is run
CMD ["uvicorn", "bank_of_tomorrow.main:app", "--host", "0.0.0.0", "--port", "8000"]