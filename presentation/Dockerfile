FROM python:3.11.5

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY app2.py /

CMD ["uvicorn", "app2:app", "--host", "0.0.0.0", "--port", "5000"]