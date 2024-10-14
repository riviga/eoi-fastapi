FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt requirements.txt
COPY ZscalerRootCertificate-2048-SHA256.crt ZscalerRootCertificate-2048-SHA256.crt
RUN export CERT_DIR=$(openssl version -d | cut -f2 -d \")/certs ; echo $CERT_DIR;  cp /code/ZscalerRootCertificate-2048-SHA256.crt $CERT_DIR; update-ca-certificates
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code
EXPOSE 8000
ENV TZ="Europe/Madrid"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
