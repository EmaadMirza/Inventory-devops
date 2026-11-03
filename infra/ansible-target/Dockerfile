FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server python3 supervisor ca-certificates && rm -rf /var/lib/apt/lists/* && mkdir -p /run/sshd /root/.ssh && chmod 700 /root/.ssh
COPY infra/ansible-target/start.sh /start.sh
RUN chmod 755 /start.sh
ENTRYPOINT ["/start.sh"]
