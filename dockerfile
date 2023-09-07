FROM python

COPY . .
#when building image
RUN pip install -r requirements.txt 

#when container is run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]