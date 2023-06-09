
FROM python


RUN apt-get update && apt-get install -y supervisor
EXPOSE 8765

COPY client.py /app/client.py
COPY web_socket_server.py /app/web_socket_server.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY runner.sh /app/runner.sh
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod +x /app/runner.sh

RUN mkdir -p /logs

CMD ./runner.sh
