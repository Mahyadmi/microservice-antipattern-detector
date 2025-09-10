FROM maven:3.8-openjdk-17

WORKDIR /workspace
COPY analyze.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/analyze.sh

CMD ["/usr/local/bin/analyze.sh"]
