FROM python:3.12-slim

WORKDIR /src

COPY requirements requirements

RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt
ENV PATH="/src/venv/bin:${PATH}"

RUN apt-get update \
    && apt-get -y install curl git gcc \
    && /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
    && (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /root/.profile \
    && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" \
    && brew install cbc \
    && brew install ipopt

ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"

COPY assets assets 
COPY pages pages 
COPY partials partials
COPY boot.sh index.py input.py pyo_model.py cbc.exe ipopt.exe .env ./

EXPOSE 8080

ENTRYPOINT [ "./boot.sh" ]