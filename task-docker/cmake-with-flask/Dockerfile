FROM ubuntu:24.04 as build

RUN apt-get update && apt-get install -y cmake g++

WORKDIR /opt/cmake-with-flask
COPY . .

RUN mkdir build && cd build && cmake .. && make

FROM ubuntu:24.04

RUN apt-get update -y && \
  apt-get install -y git python3 python3-flask

RUN bash -c "echo 'cmake-with-flask in docker' > /README.md" && \
  bash -c "echo -e '#!/bin/bash\necho Hello world' > /bin/print_hello" && \
  chmod a+x /bin/print_hello

COPY --from=build /opt/cmake-with-flask/bin /bin
COPY --from=build /opt/cmake-with-flask/lib /lib
RUN groupadd devops2024group && \
  useradd -s /bin/bash -g devops2024group devops2024user

WORKDIR /opt/cmake-with-flask/
COPY app.py .
RUN chown -R devops2024user:devops2024group /opt/cmake-with-flask

USER devops2024user

EXPOSE 8898

CMD python3 app.py --host 0.0.0.0 --port 8898
