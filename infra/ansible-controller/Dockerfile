FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openssh-client && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir ansible-core==2.18.6
WORKDIR /workspace/ansible
ENTRYPOINT ["ansible-playbook"]
