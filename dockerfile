# Pull Base Image
FROM python:3.8

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

# Install Dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

