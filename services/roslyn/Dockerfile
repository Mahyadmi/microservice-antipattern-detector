FROM mcr.microsoft.com/dotnet/sdk:8.0

RUN dotnet tool install -g dotnet-format
ENV PATH="${PATH}:/root/.dotnet/tools"

WORKDIR /workspace
COPY analyze.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/analyze.sh

CMD ["/usr/local/bin/analyze.sh"]
