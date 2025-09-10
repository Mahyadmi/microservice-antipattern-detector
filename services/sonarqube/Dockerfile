FROM sonarqube:10.3-community

USER root
RUN cd /opt/sonarqube/extensions/plugins && \
    wget -q https://github.com/checkstyle/sonar-checkstyle/releases/download/10.12.5/checkstyle-sonar-plugin-10.12.5.jar || true

USER sonarqube
ENV SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true
