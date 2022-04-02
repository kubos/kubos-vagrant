FROM kubos-dev

RUN useradd --create-home --shell /bin/bash kubos
RUN adduser kubos sudo

RUN echo 'kubos:Kubos123' | chpasswd

USER kubos
WORKDIR /home/kubos


