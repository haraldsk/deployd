FROM python:3.9

COPY --from=bitnami/kubectl:1.19 /opt/bitnami/kubectl/bin/kubectl /usr/local/bin/kubectl

WORKDIR /opt/deployd
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/

EXPOSE 8080
CMD [ "python3", "/opt/deployd/src/deployd.py" ]
