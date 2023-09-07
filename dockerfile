FROM python

COPY . .
#when building image
RUN pip install -r requirements.txt 

EXPOSE 8000
#when container is run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]