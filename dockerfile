FROM python:3.11.6
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
#when building image
RUN pip install -r requirements.txt 

#when container is run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]