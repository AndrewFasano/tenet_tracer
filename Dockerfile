FROM pandare/panda:latest

COPY run.py .

ENTRYPOINT ["python3", "run.py"]
