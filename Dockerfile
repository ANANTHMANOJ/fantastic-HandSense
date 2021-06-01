FROM python:3.7.10-slim-stretch
COPY . /home
EXPOSE 5000
WORKDIR ./home
RUN pip install --default-timeout=100 -r requirements.txt
CMD python3 HandCursor.py