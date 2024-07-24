FROM python:3.12-slim
LABEL authors="dmonster"

COPY . .

RUN pip install -r  requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]



#https://youtu.be/gBfkX9H3szQ?list =PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&t=2129