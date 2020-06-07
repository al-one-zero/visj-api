FROM python:3.7-slim
COPY api /api
WORKDIR /api
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]
