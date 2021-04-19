FROM pandare/pandadev:latest

RUN git fetch -a  && git checkout -b trace origin/trace
RUN cd build && ../build.sh

COPY run.py .

ENTRYPOINT ["python3", "run.py"]
