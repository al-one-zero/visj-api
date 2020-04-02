FROM python:3.8
COPY . /api
WORKDIR /api
RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['api.py']
