FROM python:3.11

# Install OpenJDK 17 and necessary tools
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME and update PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# Install PySpark
RUN pip install pyspark==3.5.0

# Set working directory
WORKDIR /app

# Default command
CMD ["python", "app.py"]
