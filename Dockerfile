# 1. Start with an official, lightweight Python runtime
FROM python:3.12-slim

# 2. Set an environment variable to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establish the operational directory inside the container
WORKDIR /code

# 4. Copy the requirements first to take advantage of Docker build caching
COPY ./requirements.txt /code/requirements.txt

# 5. Install all required Python frameworks and libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 6. Copy your application source code and runtime configuration parameters
COPY ./app /code/app
COPY .env /code/.env

# 7. Document that the container naturally listens on network port 8000
EXPOSE 8000

# 8. Command to trigger Uvicorn and bind it to external network traffic
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]