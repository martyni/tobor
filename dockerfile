FROM python:3.8
RUN mkdir /home/app
COPY requirements.txt /home/app
RUN pip install -r /home/app/requirements.txt
COPY . /home/app
COPY credentials /twitch_login.yaml
RUN echo "#!/bin/bash">>/bin/entrypoint.sh
RUN cat /home/app/scripts/NAME>>/bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh
RUN pip install /home/app 
CMD ["/bin/entrypoint.sh"]
