FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git curl gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Install Java and SonarScanner
RUN apt-get update && apt-get install -y default-jre-headless wget unzip && \
    cd /opt && \
    wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip && \
    unzip sonar-scanner-cli-4.8.0.2856-linux.zip && \
    ln -s /opt/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    rm sonar-scanner-cli-4.8.0.2856-linux.zip

# Copy sample microservice files for testing
COPY sample-microservice/ /app/sample-microservice/
