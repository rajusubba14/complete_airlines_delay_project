FROM --platform=linux/amd64 python:3.11 AS build


# 1) Install your dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy model artifact and inference server code into the image
COPY model/         ./model/
COPY src/deployment/inference_server.py .

# 3) Expose the port and start the Flask server
EXPOSE 8080
CMD ["python", "inference_server.py"]