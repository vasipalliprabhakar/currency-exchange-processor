FROM python:3.11
ADD . /app
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install deltalake aiohttp flatten-json
RUN python3 -m pip install -r /app/src/requirements.txt
CMD ["python3","/app/src/etl_scripts/job_runner.py"]
